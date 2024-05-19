import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
import oracledb
import fc

class CadastrarFornecedor:
    def __init__(self, root_parameter):
        self.root = root_parameter
        self.root.title("Fornecedores")
        self.connection = fc.conectar_banco()
        if self.connection:
            self.cursor = self.connection.cursor()
            self.consultar_design()
        else:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            self.root.destroy()
        self.root.mainloop()

    def carregar_fornecedores(self):
        self.tree.delete(*self.tree.get_children())
        sql = "SELECT ID, NOME, SETOR, TELEFONE, SITE FROM TBL_FORNECEDORES"
        self.cursor.execute(sql)
        fornecedores = self.cursor.fetchall()
        for fornecedor in fornecedores:
            self.tree.insert("", "end", values=fornecedor)

    def buscar_fornecedor(self):
        termo_busca = self.entry_busca.get()
        tipo_busca = self.combo_tipo_busca.get()
        if tipo_busca == "ID":
            sql = "SELECT ID, NOME, SETOR, TELEFONE, SITE FROM TBL_FORNECEDORES WHERE ID = :TERMOS_BUSCA"
        else:
            sql = "SELECT ID, NOME, SETOR, TELEFONE, SITE FROM TBL_FORNECEDORES WHERE NOME LIKE :TERMOS_BUSCA"
        self.cursor.execute(sql, {"TERMOS_BUSCA": f'%{termo_busca}%'})
        resultados = self.cursor.fetchall()
        if resultados:
            self.tree.delete(*self.tree.get_children())
            for fornecedor in resultados:
                self.tree.insert("", "end", values=fornecedor)
        else:
            messagebox.showerror("Erro", "Nenhum resultado encontrado.")

    def cadastrar_fornecedor(self):
        self.cadastro_design()

    def editar_fornecedor(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Por favor, selecione um fornecedor para editar.")
            return
        item = self.tree.item(selected_item)
        fornecedor_id = item['values'][0]
        self.cadastro_design(fornecedor_id)

    def cadastro_design(self, fornecedor_id=None):
        self.new_window = ctk.CTkToplevel(self.root)
        self.new_window.title("Cadastrar Fornecedor" if fornecedor_id is None else "Editar Fornecedor")
        
        frame_cadastro = ctk.CTkFrame(self.new_window)
        frame_cadastro.pack(padx=20, pady=20, fill="both", expand=True)
        frame_cadastro.grid_columnconfigure(0, weight=1)
        frame_cadastro.grid_columnconfigure(1, weight=3)

        entry_width = 150

        label_nome = ctk.CTkLabel(frame_cadastro, text="Nome:")
        label_nome.grid(row=0, column=0, sticky=tk.W, pady=2, padx=2)
        self.entry_nome = ctk.CTkEntry(frame_cadastro, width=entry_width)
        self.entry_nome.grid(row=0, column=1, sticky=tk.W, pady=2, padx=2)

        label_descricao = ctk.CTkLabel(frame_cadastro, text="Descrição:")
        label_descricao.grid(row=1, column=0, sticky=tk.W, pady=2, padx=2)
        self.entry_descricao = ctk.CTkEntry(frame_cadastro, width=entry_width)
        self.entry_descricao.grid(row=1, column=1, sticky=tk.W, pady=2, padx=2)

        label_setor = ctk.CTkLabel(frame_cadastro, text="Setor:")
        label_setor.grid(row=2, column=0, sticky=tk.W, pady=2, padx=2)
        self.entry_setor = ctk.CTkEntry(frame_cadastro, width=entry_width)
        self.entry_setor.grid(row=2, column=1, sticky=tk.W, pady=2, padx=2)

        label_endereco = ctk.CTkLabel(frame_cadastro, text="Endereço:")
        label_endereco.grid(row=3, column=0, sticky=tk.W, pady=2, padx=2)
        self.entry_endereco = ctk.CTkEntry(frame_cadastro, width=entry_width)
        self.entry_endereco.grid(row=3, column=1, sticky=tk.W, pady=2, padx=2)

        label_telefone = ctk.CTkLabel(frame_cadastro, text="Telefone:")
        label_telefone.grid(row=4, column=0, sticky=tk.W, pady=2, padx=2)
        self.entry_telefone = ctk.CTkEntry(frame_cadastro, width=entry_width)
        self.entry_telefone.grid(row=4, column=1, sticky=tk.W, pady=2, padx=2)

        label_email = ctk.CTkLabel(frame_cadastro, text="Email:")
        label_email.grid(row=5, column=0, sticky=tk.W, pady=2, padx=2)
        self.entry_email = ctk.CTkEntry(frame_cadastro, width=entry_width)
        self.entry_email.grid(row=5, column=1, sticky=tk.W, pady=2, padx=2)

        label_site = ctk.CTkLabel(frame_cadastro, text="Site:")
        label_site.grid(row=6, column=0, sticky=tk.W, pady=2, padx=2)
        self.entry_site = ctk.CTkEntry(frame_cadastro, width=entry_width)
        self.entry_site.grid(row=6, column=1, sticky=tk.W, pady=2, padx=2)

        buttons_frame = ctk.CTkFrame(frame_cadastro, fg_color="#2b2b2b")
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        buttons_frame.grid(row=7, column=0, columnspan=2, pady=4)

        button_cadastrar = ctk.CTkButton(buttons_frame, text="Salvar Alterações" if fornecedor_id else "Cadastrar Fornecedor", command=lambda: self.salvar_fornecedor(fornecedor_id))
        button_cadastrar.grid(row=8, column=0, padx=2, sticky=tk.W)

        button_voltar = ctk.CTkButton(buttons_frame, text="Fechar", command=self.new_window.destroy)
        button_voltar.grid(row=8, column=1, padx=2, sticky=tk.E)

        if fornecedor_id:
            self.carregar_dados_fornecedor(fornecedor_id)

    def carregar_dados_fornecedor(self, fornecedor_id):
        sql = "SELECT NOME, DESCRICAO, SETOR, ENDERECO, TELEFONE, EMAIL, SITE FROM TBL_FORNECEDORES WHERE ID = :ID"
        self.cursor.execute(sql, {"ID": fornecedor_id})
        fornecedor = self.cursor.fetchone()
        if fornecedor:
            self.entry_nome.insert(0, fornecedor[0])
            self.entry_descricao.insert(0, fornecedor[1])
            self.entry_setor.insert(0, fornecedor[2])
            self.entry_endereco.insert(0, fornecedor[3])
            self.entry_telefone.insert(0, fornecedor[4])
            self.entry_email.insert(0, fornecedor[5])
            self.entry_site.insert(0, fornecedor[6])
        else:
            messagebox.showerror("Erro", "Fornecedor não encontrado.")
            self.new_window.destroy()

    def salvar_fornecedor(self, fornecedor_id=None):
        nome = self.entry_nome.get()
        descricao = self.entry_descricao.get()
        setor = self.entry_setor.get()
        endereco = self.entry_endereco.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()
        site = self.entry_site.get()

        if not fc.validar_nvarchar2(nome, 50, 1):
            messagebox.showerror("Erro", "Nome inválido. Verifique o valor inserido.")
            return
        if not fc.validar_nvarchar2(descricao, 50, 0):
            messagebox.showerror("Erro", "Descrição inválida. Verifique o valor inserido.")
            return
        if not fc.validar_nvarchar2(setor, 100, 0):
            messagebox.showerror("Erro", "Setor inválido. Verifique o valor inserido.")
            return
        if not fc.validar_nvarchar2(endereco, 100, 0):
            messagebox.showerror("Erro", "Endereço inválido. Verifique o valor inserido.")
            return
        if not fc.validar_nvarchar2(site, 100, 0):
            messagebox.showerror("Erro", "Site inválido. Verifique o valor inserido.")
            return
        if not fc.validar_nvarchar2(email, 100, 0):
            messagebox.showerror("Erro", "Email inválido. Verifique o valor inserido.")
            return
        if not fc.validar_nvarchar2(telefone, 20, 0):
            messagebox.showerror("Erro", "Telefone inválido. Verifique o valor inserido.")
            return

        if fornecedor_id:
            sql = """
                UPDATE TBL_FORNECEDORES
                SET NOME = :NOME, DESCRICAO = :DESCRICAO, SETOR = :SETOR, ENDERECO = :ENDERECO,
                    TELEFONE = :TELEFONE, EMAIL = :EMAIL, SITE = :SITE
                WHERE ID = :ID
            """
            params = {
                "NOME": nome,
                "DESCRICAO": descricao,
                "SETOR": setor,
                "ENDERECO": endereco,
                "TELEFONE": telefone,
                "EMAIL": email,
                "SITE": site,
                "ID": fornecedor_id
            }
        else:
            sql = """
                INSERT INTO TBL_FORNECEDORES (NOME, DESCRICAO, SETOR, ENDERECO, TELEFONE, EMAIL, SITE)
                VALUES (:NOME, :DESCRICAO, :SETOR, :ENDERECO, :TELEFONE, :EMAIL, :SITE)
            """
            params = {
                "NOME": nome,
                "DESCRICAO": descricao,
                "SETOR": setor,
                "ENDERECO": endereco,
                "TELEFONE": telefone,
                "EMAIL": email,
                "SITE": site
            }

        try:
            self.cursor.execute(sql, params)
            self.connection.commit()
            messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso." if fornecedor_id else "Fornecedor cadastrado com sucesso.")
            self.new_window.destroy()  # Fecha a janela de cadastro/edição após salvar
            self.consultar_design()  # Volta para a tela de consulta após o cadastro/edição
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar fornecedor: {e}")

    def consultar_design(self):
        for widget in self.root.winfo_children():
            widget.destroy()  # Remove todos os widgets existentes

        frame = ctk.CTkFrame(self.root)  # Cria um frame principal
        frame.pack(fill=ctk.BOTH, expand=True)  # Adiciona o frame à janela principal

        label_titulo = ctk.CTkLabel(frame, text="Consulta de Fornecedores")  # Cria um rótulo com o título
        label_titulo.pack()  # Adiciona o rótulo ao frame

        frame_busca = ctk.CTkFrame(frame)  # Cria um frame para a área de busca
        frame_busca.pack(fill=tk.X)

        label_busca = ctk.CTkLabel(frame_busca, text="Buscar Fornecedor:")  # Cria um rótulo para o campo de busca
        label_busca.pack(side=tk.LEFT)  # Adiciona o rótulo ao frame de busca

        self.entry_busca = ctk.CTkEntry(frame_busca)  # Cria um campo de entrada de texto para a busca
        self.entry_busca.pack(side=ctk.LEFT, padx=5)  # Adiciona o campo de entrada ao frame de busca

        self.combo_tipo_busca = ttk.Combobox(frame_busca, values=["ID", "Nome"], state="readonly")  # Cria um combobox para selecionar o tipo de busca
        self.combo_tipo_busca.pack(side=ctk.LEFT)  # Adiciona o combobox ao frame de busca
        self.combo_tipo_busca.current(0)  # Define o valor padrão como "ID"

        button_buscar = ctk.CTkButton(frame_busca, text="Buscar", command=self.buscar_fornecedor)  # Cria um botão para iniciar a busca
        button_buscar.pack(side=ctk.LEFT, padx=5)  # Adiciona o botão de busca ao frame de busca

        button_cadastrar = ctk.CTkButton(frame_busca, text="Cadastrar Fornecedor", command=self.cadastrar_fornecedor)  # Cria um botão para cadastrar fornecedor
        button_cadastrar.pack(side=ctk.LEFT, padx=5)  # Adiciona o botão de cadastro ao frame de busca

        button_editar = ctk.CTkButton(frame_busca, text="Editar Fornecedor", command=self.editar_fornecedor)  # Cria um botão para editar fornecedor
        button_editar.pack(side=ctk.LEFT, padx=5)  # Adiciona o botão de edição ao frame de busca

        self.tree = ttk.Treeview(frame, columns=("ID", "Nome", "Setor", "Telefone", "Site"), show="headings")  # Cria uma árvore de visualização para os fornecedores
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Setor", text="Setor")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("Site", text="Site")
        self.tree.pack(fill=ctk.BOTH, expand=True)  # Adiciona a árvore ao frame principal

        self.carregar_fornecedores()  # Carrega os fornecedores ao desenhar a interface de consulta

# Executa a aplicação
if __name__ == "__main__":
    root = ctk.CTk()  # Cria a janela principal
    CadastrarFornecedor(root)  # Instancia a classe CadastrarFornecedor e inicia a aplicação
