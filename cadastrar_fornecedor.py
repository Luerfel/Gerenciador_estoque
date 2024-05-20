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

# Carrega os fornecedores no Treeview
    def carregar_fornecedores(self):
        self.tree.delete(*self.tree.get_children())
        sql = "SELECT ID, NOME, SETOR, TELEFONE, SITE FROM TBL_FORNECEDORES"
        self.cursor.execute(sql)
        fornecedores = self.cursor.fetchall()
        for fornecedor in fornecedores:
            self.tree.insert("", "end", values=fornecedor)

# Realiza a busca de fornecedores com base no termo e tipo de busca
    def buscar_fornecedor(self):
        termo_busca = self.entry_busca.get()
        tipo_busca = self.combo_tipo_busca.get()
        if tipo_busca == "ID":
            sql = "SELECT ID, NOME, SETOR, TELEFONE, SITE FROM TBL_FORNECEDORES WHERE ID = :TERMOS_BUSCA"
            termos_busca = termo_busca  # ID deve ser tratado como um número
        else:
            sql = "SELECT ID, NOME, SETOR, TELEFONE, SITE FROM TBL_FORNECEDORES WHERE NOME LIKE :TERMOS_BUSCA"
            termos_busca = f'%{termo_busca}%'
        
        self.cursor.execute(sql, {"TERMOS_BUSCA": termos_busca})
        resultados = self.cursor.fetchall()
        if resultados:
            self.tree.delete(*self.tree.get_children())
            for fornecedor in resultados:
                self.tree.insert("", "end", values=fornecedor)
        else:
            messagebox.showerror("Erro", "Nenhum resultado encontrado.")

# Abre a janela para cadastro de fornecedor
    def cadastrar_fornecedor(self):
        self.cadastro_design()

# Abre a janela para edição de fornecedor selecionado
    def editar_fornecedor(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Por favor, selecione um fornecedor para editar.")
            return
        item = self.tree.item(selected_item)
        fornecedor_id = item['values'][0]
        self.cadastro_design(fornecedor_id)

# Exclui o fornecedor selecionado
    def excluir_fornecedor(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Por favor, selecione um fornecedor para excluir.")
            return
        item = self.tree.item(selected_item)
        fornecedor_id = item['values'][0]
        fornecedor_nome = item['values'][1]

        resposta = messagebox.askyesno("Confirmar Exclusão", "Tem certeza de que deseja excluir o fornecedor selecionado?")
        if resposta:
            try:
                # Verifica se o fornecedor_id é um número
                fornecedor_id = int(fornecedor_id)
                
                # Exclui o fornecedor da tabela TBL_FORNECEDORES
                sql_excluir_fornecedor = "DELETE FROM TBL_FORNECEDORES WHERE ID = :ID"
                self.cursor.execute(sql_excluir_fornecedor, {"ID": fornecedor_id})
                
                # Remove o nome do fornecedor na tabela TBL_PRODUTOS
                sql_limpar_produtos = "UPDATE TBL_PRODUTOS SET FORNECEDOR = NULL WHERE FORNECEDOR = :NOME"
                self.cursor.execute(sql_limpar_produtos, {"NOME": fornecedor_nome})
                
                self.connection.commit()
                messagebox.showinfo("Sucesso", "Fornecedor excluído com sucesso.")
                self.carregar_fornecedores()
            except ValueError as ve:
                messagebox.showerror("Erro", f"Erro ao excluir fornecedor: {ve}")
            except oracledb.DatabaseError as e:
                self.connection.rollback()
                messagebox.showerror("Erro", f"Erro ao excluir fornecedor: {e}")

# Cria a janela de cadastro/edição de fornecedor
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

 # Carrega os dados do fornecedor selecionado para edição
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

# Salva as alterações ou cadastro de um fornecedor
    def salvar_fornecedor(self, fornecedor_id=None):
        nome = self.entry_nome.get()
        descricao = self.entry_descricao.get()
        setor = self.entry_setor.get()
        endereco = self.entry_endereco.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()
        site = self.entry_site.get()

        if not fc.validar_nvarchar2(nome, 100, 0):
            messagebox.showerror("Erro", "Nome inválido. Verifique o valor inserido.")
            return
        if nome and nome[0].isdigit():
            messagebox.showerror("Erro", "O nome não pode começar com um número.")
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
            self.new_window.destroy()
            self.consultar_design()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar fornecedor: {e}")
    def validar_campos(self, nome, descricao, setor, endereco, telefone, email, site):
        # Valida os campos de entrada
        if not fc.validar_nvarchar2(nome, 100, 0):
            messagebox.showerror("Erro", "Nome inválido. Verifique o valor inserido.")
            return False
        if nome and nome[0].isdigit():
            messagebox.showerror("Erro", "O nome não pode começar com um número.")
            return False
        if not fc.validar_nvarchar2(descricao, 50, 0):
            messagebox.showerror("Erro", "Descrição inválida. Verifique o valor inserido.")
            return False
        if not fc.validar_nvarchar2(setor, 100, 0):
            messagebox.showerror("Erro", "Setor inválido. Verifique o valor inserido.")
            return False
        if not fc.validar_nvarchar2(endereco, 100, 0):
            messagebox.showerror("Erro", "Endereço inválido. Verifique o valor inserido.")
            return False
        if not fc.validar_nvarchar2(site, 100, 0):
            messagebox.showerror("Erro", "Site inválido. Verifique o valor inserido.")
            return False
        if not fc.validar_nvarchar2(email, 100, 0):
            messagebox.showerror("Erro", "Email inválido. Verifique o valor inserido.")
            return False
        if not fc.validar_nvarchar2(telefone, 20, 0):
            messagebox.showerror("Erro", "Telefone inválido. Verifique o valor inserido.")
            return False
        return True
    
    def configurar_treeview(self, frame):
        # Configura a árvore (Treeview) para exibir os fornecedores
        self.tree = ttk.Treeview(frame, columns=("ID", "Nome", "Setor", "Telefone", "Site"), show="headings")
        self.tree.heading("ID", text="ID", anchor="center")
        self.tree.heading("Nome", text="Nome", anchor="center")
        self.tree.heading("Setor", text="Setor", anchor="center")
        self.tree.heading("Telefone", text="Telefone", anchor="center")
        self.tree.heading("Site", text="Site", anchor="center")
        self.tree.column("ID", anchor="center")
        self.tree.column("Nome", anchor="center")
        self.tree.column("Setor", anchor="center")
        self.tree.column("Telefone", anchor="center")
        self.tree.column("Site", anchor="center")
        self.tree.pack(fill=ctk.BOTH, expand=True)


# Interface principal para consulta de fornecedores       
    def consultar_design(self):
        # Configura a janela de consulta de fornecedores
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ctk.CTkFrame(self.root)
        frame.pack(fill=ctk.BOTH, expand=True)

        label_titulo = ctk.CTkLabel(frame, text="Consulta de Fornecedores")
        label_titulo.pack()

        frame_busca = ctk.CTkFrame(frame)
        frame_busca.pack(fill=tk.X)

        label_busca = ctk.CTkLabel(frame_busca, text="Buscar Fornecedor:")
        label_busca.pack(side=tk.LEFT)

        self.entry_busca = ctk.CTkEntry(frame_busca)
        self.entry_busca.pack(side=ctk.LEFT, padx=5)

        self.combo_tipo_busca = ttk.Combobox(frame_busca, values=["ID", "Nome"], state="readonly")
        self.combo_tipo_busca.pack(side=ctk.LEFT)
        self.combo_tipo_busca.current(0)

        button_buscar = ctk.CTkButton(frame_busca, text="Buscar", command=self.buscar_fornecedor)
        button_buscar.pack(side=ctk.LEFT, padx=5)

        button_cadastrar = ctk.CTkButton(frame_busca, text="Cadastrar Fornecedor", command=self.cadastrar_fornecedor)
        button_cadastrar.pack(side=ctk.LEFT, padx=5)

        button_editar = ctk.CTkButton(frame_busca, text="Editar Fornecedor", command=self.editar_fornecedor)
        button_editar.pack(side=ctk.LEFT, padx=5)

        button_excluir = ctk.CTkButton(frame_busca, text="Excluir Fornecedor", command=self.excluir_fornecedor)
        button_excluir.pack(side=ctk.LEFT, padx=5)

        self.configurar_treeview(frame)
        self.carregar_fornecedores()

if __name__ == "__main__":
    root = ctk.CTk()
    CadastrarFornecedor(root)
