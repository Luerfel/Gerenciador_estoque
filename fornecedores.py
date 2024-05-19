import tkinter as tk  # Biblioteca padrão do Tkinter para a criação de interfaces gráficas
import customtkinter as ctk  # Biblioteca customizada para estilização do Tkinter
from tkinter import ttk, messagebox  # Importa componentes adicionais do Tkinter
import oracledb  # Biblioteca para conectar-se ao banco de dados Oracle
import fc

# Classe para a janela de consulta de fornecedores
class CadastrarFornecedor:
    def __init__(self, root_parameter):
        self.root = root_parameter  # Janela principal da aplicação
        self.root.title("Fornecedores")  # Define o título da janela
        self.connection = fc.conectar_banco()  # Conecta ao banco de dados
        if self.connection:
            self.cursor = self.connection.cursor()
            self.consultar_design()  # Chama o método para desenhar a interface
        else:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            self.root.destroy()
        self.root.mainloop()  # Inicia o loop principal da interface gráfica

    # Método para carregar os fornecedores do banco de dados na árvore de visualização
    def carregar_fornecedores(self):
        self.tree.delete(*self.tree.get_children())  # Limpa os resultados anteriores da árvore
        sql = "SELECT ID, NOME, SETOR, TELEFONE, SITE FROM TBL_FORNECEDORES"
        self.cursor.execute(sql)  # Executa o comando SQL
        fornecedores = self.cursor.fetchall()  # Busca todos os resultados da consulta
        for fornecedor in fornecedores:  # Itera sobre os fornecedores retornados
            self.tree.insert("", "end", values=fornecedor)  # Insere os fornecedores na árvore

    # Método para buscar um fornecedor específico no banco de dados
    def buscar_fornecedor(self):
        termo_busca = self.entry_busca.get()  # Obtém o termo de busca inserido pelo usuário
        tipo_busca = self.combo_tipo_busca.get()  # Obtém o tipo de busca selecionado pelo usuário
        if tipo_busca == "ID":  # Verifica se a busca é por ID
            sql = "SELECT ID, NOME, SETOR, TELEFONE, SITE FROM TBL_FORNECEDORES WHERE ID = :TERMOS_BUSCA"
        else:  # Caso contrário, a busca será por nome
            sql = "SELECT ID, NOME, SETOR, TELEFONE, SITE FROM TBL_FORNECEDORES WHERE NOME LIKE :TERMOS_BUSCA"
        self.cursor.execute(sql, {"TERMOS_BUSCA": f'%{termo_busca}%'})  # Executa o comando SQL com o termo de busca
        resultados = self.cursor.fetchall()
        if resultados:
            self.tree.delete(*self.tree.get_children())  # Limpa os resultados anteriores da árvore
            for fornecedor in resultados:
                self.tree.insert("", "end", values=fornecedor)  # Insere os fornecedores encontrados na árvore
        else:
            messagebox.showerror("Erro", "Nenhum resultado encontrado.")  # Exibe uma mensagem de erro se nenhum resultado for encontrado

    # Método para cadastrar um novo fornecedor
    def cadastrar_fornecedor(self):
        self.cadastro_design()

    # Método para desenhar a interface de cadastro de fornecedores
    def cadastro_design(self):
        # Desenha a interface de cadastro
        frame = ctk.CTkFrame(self.root)
        frame.place(relwidth=1, relheight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=3)

        # Nome do fornecedor
        label_nome = ctk.CTkLabel(frame, text="Nome:")
        label_nome.grid(row=0, column=0, sticky=tk.W, pady=7, padx=15)
        self.entry_nome = ctk.CTkEntry(frame)
        self.entry_nome.grid(row=0, column=1, sticky=tk.EW, pady=7, padx=15)

        # Descrição do fornecedor
        label_descricao = ctk.CTkLabel(frame, text="Descrição:")
        label_descricao.grid(row=1, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_descricao = ctk.CTkEntry(frame)
        self.entry_descricao.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=15)

        # Setor do fornecedor
        label_setor = ctk.CTkLabel(frame, text="Setor:")
        label_setor.grid(row=2, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_setor = ctk.CTkEntry(frame)
        self.entry_setor.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=15)

        # Endereço do fornecedor
        label_endereco = ctk.CTkLabel(frame, text="Endereço:")
        label_endereco.grid(row=3, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_endereco = ctk.CTkEntry(frame)
        self.entry_endereco.grid(row=3, column=1, sticky=tk.EW, pady=5, padx=15)

        # Telefone do fornecedor
        label_telefone = ctk.CTkLabel(frame, text="Telefone:")
        label_telefone.grid(row=4, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_telefone = ctk.CTkEntry(frame)
        self.entry_telefone.grid(row=4, column=1, sticky=tk.EW, pady=5, padx=15)

        # Email do fornecedor
        label_email = ctk.CTkLabel(frame, text="Email:")
        label_email.grid(row=5, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_email = ctk.CTkEntry(frame)
        self.entry_email.grid(row=5, column=1, sticky=tk.EW, pady=5, padx=15)

        # Site do fornecedor
        label_site = ctk.CTkLabel(frame, text="Site:")
        label_site.grid(row=6, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_site = ctk.CTkEntry(frame)
        self.entry_site.grid(row=6, column=1, sticky=tk.EW, pady=5, padx=15)

        # Frame para botões de ação
        buttons_frame = ctk.CTkFrame(frame, fg_color="#2b2b2b")
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        buttons_frame.grid(row=7, column=0, columnspan=2, pady=4)

        # Botão para cadastrar o fornecedor
        button_cadastrar = ctk.CTkButton(buttons_frame, text="Cadastrar Fornecedor", command=self.salvar_fornecedor)
        button_cadastrar.grid(row=0, column=0, padx=5, sticky=tk.W)

        # Botão para voltar à tela de consulta
        button_voltar = ctk.CTkButton(buttons_frame, text="Voltar", command=self.consultar_design)
        button_voltar.grid(row=0, column=1, padx=5, sticky=tk.E)

    # Método para salvar o fornecedor no banco de dados
    def salvar_fornecedor(self):
        nome = self.entry_nome.get()
        descricao = self.entry_descricao.get()
        setor = self.entry_setor.get()
        endereco = self.entry_endereco.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()
        site = self.entry_site.get()

        # Validações dos campos
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

        sql = """
            INSERT INTO TBL_FORNECEDORES (NOME, DESCRICAO, SETOR, ENDERECO, TELEFONE, EMAIL, SITE)
            VALUES (:NOME, :DESCRICAO, :SETOR, :ENDERECO, :TELEFONE, :EMAIL, :SITE)
        """
        try:
            self.cursor.execute(sql, {
                "NOME": nome,
                "DESCRICAO": descricao,
                "SETOR": setor,
                "ENDERECO": endereco,
                "TELEFONE": telefone,
                "EMAIL": email,
                "SITE": site
            })
            self.connection.commit()
            messagebox.showinfo("Sucesso", "Fornecedor cadastrado com sucesso.")
            self.consultar_design()  # Volta para a tela de consulta após o cadastro
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar fornecedor: {e}")

    # Método para desenhar a interface de consulta de fornecedores
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
