import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import oracledb
from commons import Commons

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


class EditarProduto(Commons):
    def __init__(self, root_parameter):
        # Inicializa a janela principal da aplicação
        self.root = root_parameter
        self.root.title("Editar Produto")
        self.codigo_de_barras = None  
        self.root.protocol("WM_DELETE_WINDOW", self.confirm_exit)  # Define o comportamento ao fechar a janela
        self.editar_design()  # Configura o design da interface
        self.root.mainloop()  # Mantém a aplicação em execução

    def fechar_janela_editar_produto(self):
        # Restaura a janela principal e fecha a janela de edição
        self.root.deiconify()
        self.nova_janela.destroy()

    def consultar_banco_de_dados(self, codigo):
        # Consulta o banco de dados para obter as informações do produto pelo código de barras
        sql = """
            SELECT COUNT(*) FROM tbl_produtos WHERE codigo_de_barras = :CODIGO_DE_BARRAS
            """
        cursor.execute(sql, {"CODIGO_DE_BARRAS": codigo})
        resultado = cursor.fetchone()[0]
        # Verifica se o produto existe
        if resultado != 1:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return

        sql = """
        SELECT nome, descricao, preco_de_compra, preco_de_venda, unidades, fornecedor 
        FROM tbl_produtos WHERE codigo_de_barras = :CODIGO_DE_BARRAS 
        """
        cursor.execute(sql, {"CODIGO_DE_BARRAS": codigo})
        produto = cursor.fetchone()  # Obtém os dados do produto da consulta
        if produto:
            self.editar_produto()  # Chama o método para editar o produto
            # Preenche os campos na interface gráfica com os dados do produto
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, produto[0])
            self.entry_descricao.delete(0, tk.END)
            self.entry_descricao.insert(0, produto[1])
            self.entry_custo_aquisicao.delete(0, tk.END)
            self.entry_custo_aquisicao.insert(0, str(produto[2]))
            self.entry_preco_venda_principal.delete(0, tk.END)
            self.entry_preco_venda_principal.insert(0, str(produto[3]))
            self.entry_unidades.delete(0, tk.END)
            self.entry_unidades.insert(0, str(produto[4]))
            self.combo_fornecedor.set(produto[5])

    def selecionar_produto(self):
        # Obtém o código de barras inserido pelo usuário e consulta o banco de dados
        self.codigo_de_barras = self.entry_codigo_de_barras.get()

        if not self.codigo_de_barras:
            messagebox.showerror("Erro", "Código de barras inválido.")
            return

        self.consultar_banco_de_dados(self.codigo_de_barras)

    def atualizar_produto(self):
        # Obtém os novos dados do produto inseridos pelo usuário e atualiza o banco de dados
        nome = self.entry_nome.get()
        descricao = self.entry_descricao.get()
        preco_compra = float(self.entry_custo_aquisicao.get())
        preco_venda = float(self.entry_preco_venda_principal.get())
        unidades = int(self.entry_unidades.get())
        fornecedor = self.combo_fornecedor.get()

        sql = """
        UPDATE tbl_produtos 
        SET nome = :nome, descricao = :descricao, preco_de_compra = :preco_compra, 
        preco_de_venda = :preco_venda, unidades = :unidades, fornecedor = :fornecedor 
        WHERE codigo_de_barras = :CODIGO_DE_BARRAS
        """
        cursor.execute(sql, {
            "nome": nome,
            "descricao": descricao,
            "preco_compra": preco_compra,
            "preco_venda": preco_venda,
            "unidades": unidades,
            "fornecedor": fornecedor,
            "CODIGO_DE_BARRAS": self.codigo_de_barras
        })
        connection.commit()
        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso.")

    def editar_produto(self):
        # Cria uma nova janela para edição do produto
        self.root.iconify()  # Minimiza a janela principal
        self.nova_janela = tk.Toplevel(self.root)
        self.nova_janela.title("Editar Produto")
        self.nova_janela.config(bg="#2b2b2b")
        self.nova_janela.protocol("WM_DELETE_WINDOW", self.fechar_janela_editar_produto)  # Define o comportamento ao fechar a janela

        # Adiciona conteúdo à nova janela
        frame = ctk.CTkFrame(self.nova_janela)
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Campos de entrada para os dados do produto
        label_nome = ctk.CTkLabel(frame, text="Nome:")
        label_nome.grid(row=0, column=0, sticky=tk.W)
        self.entry_nome = ctk.CTkEntry(frame, width=50)
        self.entry_nome.grid(row=0, column=1, sticky=tk.W)

        label_descricao = ctk.CTkLabel(frame, text="Descrição:")
        label_descricao.grid(row=1, column=0, sticky=tk.W)
        self.entry_descricao = ctk.CTkEntry(frame, width=50)
        self.entry_descricao.grid(row=1, column=1, sticky=tk.W)

        label_custo_aquisicao = ctk.CTkLabel(frame, text="Custo de Aquisição:")
        label_custo_aquisicao.grid(row=2, column=0, sticky=tk.W)
        self.entry_custo_aquisicao = ctk.CTkEntry(frame, width=50)
        self.entry_custo_aquisicao.grid(row=2, column=1, sticky=tk.W)

        label_unidades = ctk.CTkLabel(frame, text="Unidades:")
        label_unidades.grid(row=3, column=0, sticky=tk.W)
        self.entry_unidades = ctk.CTkEntry(frame, width=50)
        self.entry_unidades.grid(row=3, column=1, sticky=tk.W)

        label_fornecedor = ctk.CTkLabel(frame, text="Fornecedor:")
        label_fornecedor.grid(row=4, column=0, sticky=tk.W)
        self.combo_fornecedor = ctk.CTkComboBox(frame, width=47, state="readonly")
        self.combo_fornecedor['values'] = ("Fornecedor 1", "Fornecedor 2", "Fornecedor 3")  # Adicione os fornecedores
        self.combo_fornecedor.grid(row=4, column=1, sticky=tk.W)

        label_preco_venda_principal = ctk.CTkLabel(frame, text="Preço de Venda:")
        label_preco_venda_principal.grid(row=5, column=0, sticky=tk.W)
        self.entry_preco_venda_principal = ctk.CTkEntry(frame, width=50)
        self.entry_preco_venda_principal.grid(row=5, column=1, sticky=tk.W)

        # Botão para atualizar os dados do produto
        button_atualizar = ctk.CTkButton(frame, text="Atualizar Produto", command=self.atualizar_produto)
        button_atualizar.grid(row=6, column=0, columnspan=2, pady=10)

    def editar_design(self):
        # Configura o design da interface de edição
        frame = ctk.CTkFrame(self.root)
        frame.place(relx=1, rely=1)
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Campo de entrada para o código de barras do produto
        label_codigo_de_barras = ctk.CTkLabel(frame, text="Digite o código de barras do produto:", text_color="white")
        label_codigo_de_barras.grid(row=0, column=0, sticky=tk.W, padx=4, pady=3)
        self.entry_codigo_de_barras = ctk.CTkEntry(frame, width=100)
        self.entry_codigo_de_barras.grid(row=0, column=1, sticky=tk.W, padx=4, pady=3)

        # Botão para encontrar o produto pelo código de barras
        button_encontrar_produto = ctk.CTkButton(frame, text="Procurar Produto", command=self.selecionar_produto,
                                                 text_color="white")
        button_encontrar_produto.grid(row=1, column=0, columnspan=2, pady=10)


if __name__ == "__main__":
    # Inicializa a aplicação
    root = ctk.CTk()
    EditarProduto(root)
