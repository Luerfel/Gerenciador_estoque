import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import oracledb

# biblioteca da oracle

# Estabelece a conexão com o banco de dados Oracle.

# **Observações:**

# * Este código utiliza um banco de dados local para armazenar as informações.
# * Altere as variáveis `user`, `password`, `dsn` e `sid` para conectar-se ao seu banco de dados.

# **Detalhes da conexão:**

# * **user:** Nome de usuário do banco de dados.
# * **password:** Senha do banco de dados.
# * **host:** Nome do serviço do banco de dados.
# * **sid:** SID (System Identifier) do banco de dados.

# Caso seja a primeira vez Por favor Gere a tabela com o GerarTabela.py

connection = oracledb.connect(user="SYSTEM", password="senha", host="localhost", port=1521)
cursor = connection.cursor()


class editar_produto():
    def __init__(self, root_parameter):
        # Inicializa a janela principal da aplicação
        self.root = root_parameter
        self.root.title("Editar Produto")
        # Chama o método para configurar o design da interface
        self.editar_design()
        # Carrega os produtos na árvore
        self.carregar_produtos()
        # Mantém a aplicação em execução
        self.root.mainloop()

    def carregar_produtos(self):
        # Consulta o banco de dados para obter os produtos e carrega-os na árvore
        sql = "SELECT codigo_de_barras, nome FROM tbl_produtos"
        cursor.execute(sql)
        produtos = cursor.fetchall()
        for produto in produtos:
            self.codigo, nome = produto
            self.tree.insert("", "end", values=(self.codigo, nome))

    def editar_produtodesign(self):
        # Configura o design da interface de editar de produtos
        frame = ctk.CTkFrame(self.root)
        frame.place(relwidth=1, relheight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=3)

        # Campos de entrada para dados do produto
        label_nome = ctk.CTkLabel(frame, text="Nome:")
        label_nome.grid(row=0, column=0, sticky=tk.W, pady=7, padx=15)
        self.entry_nome = ctk.CTkEntry(frame)
        self.entry_nome.grid(row=0, column=1, sticky=tk.EW, pady=7, padx=15)

        label_descricao = ctk.CTkLabel(frame, text="Descrição:")
        label_descricao.grid(row=1, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_descricao = ctk.CTkEntry(frame)
        self.entry_descricao.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=15)

        label_custo_aquisicao = ctk.CTkLabel(frame, text="Custo de Aquisição:")
        label_custo_aquisicao.grid(row=2, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_custo_aquisicao = ctk.CTkEntry(frame)
        self.entry_custo_aquisicao.grid(row=2, sticky=tk.EW, column=1, pady=5, padx=15)

        label_unidades = ctk.CTkLabel(frame, text="Unidades:")
        label_unidades.grid(row=3, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_unidades = ctk.CTkEntry(frame)
        self.entry_unidades.grid(row=3, column=1, sticky=tk.EW, pady=5, padx=15)

        label_fornecedor = ctk.CTkLabel(frame, text="Fornecedor:")
        label_fornecedor.grid(row=4, column=0, sticky=tk.W, pady=5, padx=15)
        self.combo_fornecedor = ctk.CTkComboBox(frame, state="readonly", values=["Fornecedor 1", "Fornecedor 2", "Fornecedor 3"])  # Aqui você pode adicionar os fornecedores cadastrados
        self.combo_fornecedor.grid(row=4, column=1, sticky=tk.EW, pady=5, padx=15)

        label_preco_venda_principal = ctk.CTkLabel(frame, text="Preço de Venda:")
        label_preco_venda_principal.grid(row=5, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_preco_venda_principal = ctk.CTkEntry(frame)
        self.entry_preco_venda_principal.grid(row=5, sticky=tk.EW, column=1, pady=5, padx=15)

        # Frame para botões
        buttons_frame = ctk.CTkFrame(frame, fg_color="#2b2b2b")
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        buttons_frame.grid(row=6, column=0, columnspan=2, pady=4)

        # Botão para editar
        button_cadastrar = ctk.CTkButton(buttons_frame, text="Editar Produto", command=self.confirmar_editar)
        button_cadastrar.grid(row=0, column=0, padx=5, sticky=tk.W)
    
    def confirmar_editar(self):
        print()

    def buscar_produto(self):
        # Busca um produto pelo código
        codigo_busca = self.entry_codigo.get()
        sql = "SELECT codigo_de_barras, nome FROM tbl_produtos WHERE codigo_de_barras = :CODIGO_DE_BARRAS"
        cursor.execute(sql, {"CODIGO_DE_BARRAS": codigo_busca})
        produto = cursor.fetchone()
        if produto:
            self.codigo, self.nome = produto
            # Limpa a árvore e exibe o produto encontrado
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=(self.codigo, self.nome))
        else:
            # Exibe uma mensagem de erro se o produto não for encontrado
            messagebox.showerror("Erro", "Produto não encontrado.")

    def editar_design(self):
        # Configura o design da interface gráfica
        self.frame = ctk.CTkFrame(self.root)
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Adiciona um título à janela
        label_titulo = ctk.CTkLabel(self.frame, text="Lista de Produtos",text_color="#f9f6ee")
        label_titulo.grid(row=0, column=0, sticky=tk.W)

        # Cria uma árvore para exibir os produtos
        self.tree = ttk.Treeview(self.frame, columns=("Código de Barras", "Nome"), show="headings")
        self.tree.column("0",minwidth=0,width=280)
        self.tree.column("1",minwidth=0,width=280)
        self.tree.heading("Código de Barras", text="Código de Barras")
        self.tree.heading("Nome", text="Nome")
        self.tree.grid(row=0, column=0, sticky=tk.W)

        # Configura o frame para busca de produto
        frame_busca = ctk.CTkFrame(self.frame, fg_color="#2b2b2b")
        frame_busca.place(relwidth=1, relheight=1)
        frame_busca.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame_busca.columnconfigure(0, weight=1)

        # Adiciona um campo de entrada e um botão para buscar produto por código
        label_codigo = ctk.CTkLabel(frame_busca, text="Código do Produto:", fg_color="#2b2b2b")
        label_codigo.grid(row=1, columnspan=2, sticky=tk.W,padx=3)
        self.entry_codigo = ctk.CTkEntry(frame_busca)
        self.entry_codigo.grid(row=1, column=1, sticky=tk.W)

        button_buscar = ctk.CTkButton(frame_busca, text="Buscar Produto", command=self.buscar_produto)
        button_buscar.grid(row=1, column=2, sticky=tk.W,padx=5)
        
        # Adiciona um botão para editar produto
        button_excluir = ctk.CTkButton(frame_busca, text="Editar Produto", command=self.editar_produtodesign)
        button_excluir.grid(row=1, column=3, sticky=tk.W, padx=5)

if __name__ == "__main__":
    # Inicia a aplicação
    root = ctk.CTk()
    editar_produto(root)
