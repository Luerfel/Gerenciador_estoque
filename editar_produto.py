import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import fc
from calculo_venda import CalculadoraPrecoVenda

class EditarProduto():
    def __init__(self, root_parameter):
        self.root = root_parameter
        self.root.title("Editar Produto")
        self.root.resizable(False, False)
        self.codigo = None  # Armazena o código do produto que está sendo editado
        self.connection = fc.conectar_banco()
        if not self.connection:
            self.root.destroy()  # Fecha a aplicação se a conexão falhar
            return
        self.cursor = self.connection.cursor()
        self.inicializar_interface()
        self.carregar_produtos()
        self.root.mainloop()

    def inicializar_interface(self):
        # Inicializa a interface principal de seleção de produtos
        self.frame = ctk.CTkFrame(self.root)
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        label_titulo = ctk.CTkLabel(self.frame, text="Lista de Produtos", text_color="#f9f6ee")
        label_titulo.grid(row=0, column=0, sticky=tk.W)

        # Treeview para exibir a lista de produtos
        self.tree = ttk.Treeview(self.frame, columns=("Código de Barras", "Nome"), show="headings")
        self.tree.column("Código de Barras", minwidth=0, width=280)
        self.tree.column("Nome", minwidth=0, width=280)
        self.tree.heading("Código de Barras", text="Código de Barras")
        self.tree.heading("Nome", text="Nome")
        self.tree.grid(row=1, column=0, sticky=tk.W)
        self.tree.bind("<ButtonRelease-1>", self.carregar_dados_produto)

        # Frame para os campos de busca e botões de ação
        frame_busca = ctk.CTkFrame(self.frame, fg_color="#2b2b2b")
        frame_busca.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame_busca.columnconfigure(0, weight=1)

        # Campo e botão para buscar produto pelo código
        label_codigo = ctk.CTkLabel(frame_busca, text="Código do Produto:", fg_color="#2b2b2b")
        label_codigo.grid(row=0, column=0, sticky=tk.W, padx=3)
        self.entry_codigo = ctk.CTkEntry(frame_busca)
        self.entry_codigo.grid(row=0, column=1, sticky=tk.W)
        button_buscar = ctk.CTkButton(frame_busca, text="Buscar Produto", command=self.buscar_produto)
        button_buscar.grid(row=0, column=2, sticky=tk.W, padx=5)

        # Botão para editar produto
        button_editar = ctk.CTkButton(frame_busca, text="Editar Produto", command=self.iniciar_edicao)
        button_editar.grid(row=0, column=3, sticky=tk.W, padx=5)

    def acessar_calculadora_preco_venda(self):
        # Método para acessar a calculadora de preço de venda e ocultar a janela principal
        self.root.withdraw()
        calculadora = CalculadoraPrecoVenda(self.root, self.entry_preco_venda_principal)

    def carregar_produtos(self):
        # Método para carregar produtos do banco de dados e exibí-los na treeview
        self.tree.delete(*self.tree.get_children())  # Limpa a treeview
        sql = "SELECT codigo_de_barras, nome FROM tbl_produtos"
        self.cursor.execute(sql)
        produtos = self.cursor.fetchall()
        for produto in produtos:
            codigo, nome = produto
            self.tree.insert("", "end", values=(codigo, nome))

    def carregar_dados_produto(self, event=None):
        # Método chamado quando um produto é selecionado na treeview
        selected_item = self.tree.selection()
        if selected_item:
            codigo = self.tree.item(selected_item[0], "values")[0]
            self.codigo = codigo

    def carregar_produto_selecionado(self):
        # Método para carregar os dados do produto selecionado nos campos de entrada
        if self.codigo:
            sql = """
            SELECT codigo_de_barras, nome, descricao, preco_de_compra, unidades, fornecedor, preco_de_venda
            FROM tbl_produtos
            WHERE codigo_de_barras = :CODIGO_DE_BARRAS
            """
            self.cursor.execute(sql, {"CODIGO_DE_BARRAS": self.codigo})
            produto = self.cursor.fetchone()
            if produto:
                codigo, nome, descricao, preco_de_compra, unidades, fornecedor, preco_de_venda = produto
                self.entry_nome.delete(0, tk.END)
                self.entry_nome.insert(0, nome)
                self.entry_descricao.delete(0, tk.END)
                self.entry_descricao.insert(0, descricao)
                self.entry_custo_aquisicao.delete(0, tk.END)
                self.entry_custo_aquisicao.insert(0, preco_de_compra)
                self.entry_unidades.delete(0, tk.END)
                self.entry_unidades.insert(0, unidades)
                self.combo_fornecedor.set(fornecedor)
                self.entry_preco_venda_principal.delete(0, tk.END)
                self.entry_preco_venda_principal.insert(0, preco_de_venda)
            else:
                messagebox.showerror("Erro", "Produto não encontrado.")

    def atualizar_produto(self):
        # Método para atualizar os dados do produto no banco de dados
        if self.codigo:
            # Obtém os valores dos campos de entrada
            nome = self.entry_nome.get()
            descricao = self.entry_descricao.get()
            preco_de_compra = self.entry_custo_aquisicao.get()
            unidades = self.entry_unidades.get()
            fornecedor = self.combo_fornecedor.get()
            preco_de_venda = self.entry_preco_venda_principal.get()

            # Validações dos campos
            if not fc.validar_nvarchar2(nome, 50, 1):
                return
            if not fc.validar_nvarchar2(descricao, 50, 0):
                return
            if not fc.validar_number("preço de venda", preco_de_venda, 1):
                return
            if not fc.validar_number("preço de compra", preco_de_compra, 1):
                return
            if not fc.validar_number("unidades", unidades, 1):
                return

            # Converte valores para tipos apropriados
            preco_de_venda = float(preco_de_venda.replace(',', '.'))
            preco_de_compra = float(preco_de_compra.replace(',', '.'))
            unidades = int(unidades.replace(',', '.'))

            try:
                # Atualiza os dados do produto no banco de dados
                sql = """
                UPDATE tbl_produtos
                SET nome = :NOME, descricao = :DESCRICAO, preco_de_compra = :PRECO_DE_COMPRA, unidades = :UNIDADES,
                    fornecedor = :FORNECEDOR, preco_de_venda = :PRECO_DE_VENDA
                WHERE codigo_de_barras = :CODIGO_DE_BARRAS
                """
                self.cursor.execute(sql, {
                    "NOME": nome,
                    "DESCRICAO": descricao,
                    "PRECO_DE_COMPRA": preco_de_compra,
                    "UNIDADES": unidades,
                    "FORNECEDOR": fornecedor,
                    "PRECO_DE_VENDA": preco_de_venda,
                    "CODIGO_DE_BARRAS": self.codigo
                })
                self.connection.commit()
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso.")

                # Fecha a janela de edição e volta para a lista de produtos
                self.frame_editar.destroy()
                self.carregar_produtos()  # Recarrega a lista de produtos
            except Exception as e:
                self.connection.rollback()
                messagebox.showerror("Erro", str(e))

    def iniciar_edicao(self):
        # Método para iniciar a edição de um produto selecionado
        if not self.codigo:
            messagebox.showerror("Erro", "Nenhum produto selecionado para edição.")
            return

        self.frame_editar = ctk.CTkFrame(self.root)
        self.frame_editar.place(relwidth=1, relheight=1)
        self.frame_editar.grid_columnconfigure(0, weight=1)
        self.frame_editar.grid_columnconfigure(1, weight=3)

        # Nome do produto
        label_nome = ctk.CTkLabel(self.frame_editar, text="Nome:")
        label_nome.grid(row=0, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_nome = ctk.CTkEntry(self.frame_editar)
        self.entry_nome.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=15)

        # Descrição do produto
        label_descricao = ctk.CTkLabel(self.frame_editar, text="Descrição:")
        label_descricao.grid(row=1, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_descricao = ctk.CTkEntry(self.frame_editar)
        self.entry_descricao.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=15)

        # Custo de aquisição do produto
        label_custo_aquisicao = ctk.CTkLabel(self.frame_editar, text="Custo de Aquisição:")
        label_custo_aquisicao.grid(row=2, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_custo_aquisicao = ctk.CTkEntry(self.frame_editar)
        self.entry_custo_aquisicao.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=15)

        # Unidades do produto
        label_unidades = ctk.CTkLabel(self.frame_editar, text="Unidades:")
        label_unidades.grid(row=3, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_unidades = ctk.CTkEntry(self.frame_editar)
        self.entry_unidades.grid(row=3, column=1, sticky=tk.EW, pady=5, padx=15)

        # Fornecedor do produto
        label_fornecedor = ctk.CTkLabel(self.frame_editar, text="Fornecedor:")
        label_fornecedor.grid(row=4, column=0, sticky=tk.W, pady=5, padx=15)
        self.combo_fornecedor = ctk.CTkComboBox(self.frame_editar, values=["Fornecedor A", "Fornecedor B", "Fornecedor C"])
        self.combo_fornecedor.grid(row=4, column=1, sticky=tk.EW, pady=5, padx=15)

        # Preço de venda do produto
        label_preco_venda_principal = ctk.CTkLabel(self.frame_editar, text="Preço de Venda:")
        label_preco_venda_principal.grid(row=5, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_preco_venda_principal = ctk.CTkEntry(self.frame_editar)
        self.entry_preco_venda_principal.grid(row=5, column=1, sticky=tk.EW, pady=5, padx=15)

        # Botões
        button_calcular_preco_venda = ctk.CTkButton(self.frame_editar, text="Calcular Preço de Venda", command=self.acessar_calculadora_preco_venda)
        button_calcular_preco_venda.grid(row=5, column=2, pady=7, padx=5, sticky=tk.W)
        button_confirmar_edicao = ctk.CTkButton(self.frame_editar, text="Confirmar", command=self.atualizar_produto)
        button_confirmar_edicao.grid(row=6, column=1, pady=7, padx=5, sticky=tk.E)

        # Carregar os dados do produto selecionado
        self.carregar_produto_selecionado()

    def buscar_produto(self):
        # Método para buscar um produto no banco de dados pelo código de barras
        codigo_busca = self.entry_codigo.get()
        sql = "SELECT codigo_de_barras, nome, descricao, preco_de_compra, unidades, fornecedor, preco_de_venda FROM tbl_produtos WHERE codigo_de_barras = :CODIGO_DE_BARRAS"
        self.cursor.execute(sql, {"CODIGO_DE_BARRAS": codigo_busca})
        produto = self.cursor.fetchone()
        if produto:
            # Preenche os campos de entrada com os dados do produto encontrado
            self.codigo, nome, descricao, preco_de_compra, unidades, fornecedor, preco_de_venda = produto
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, nome)
            self.entry_descricao.delete(0, tk.END)
            self.entry_descricao.insert(0, descricao)
            self.entry_custo_aquisicao.delete(0, tk.END)
            self.entry_custo_aquisicao.insert(0, preco_de_compra)
            self.entry_unidades.delete(0, tk.END)
            self.entry_unidades.insert(0, unidades)
            self.combo_fornecedor.set(fornecedor)
            self.entry_preco_venda_principal.delete(0, tk.END)
            self.entry_preco_venda_principal.insert(0, preco_de_venda)
            # Limpa a treeview e insere o produto encontrado
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=(self.codigo, nome))
        else:
            messagebox.showerror("Erro", "Produto não encontrado.")

if __name__ == "__main__":
    root = ctk.CTk()
    EditarProduto(root)
