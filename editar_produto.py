import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import fc
import oracledb
from calculo_venda import CalculadoraPrecoVenda
from cp import HillCipher

class EditarProduto():
    def __init__(self, root_parameter):
        self.root = root_parameter
        self.root.title("Editar Produto")
        self.root.geometry("600x300")
        self.root.resizable(False, False)
        self.root.geometry("600x300")
        self.codigo = None  # Armazena o código do produto que está sendo editado
        self.connection = fc.conectar_banco()
        if not self.connection:
            self.root.destroy()  # Fecha a aplicação se a conexão falhar
            return
        self.cursor = self.connection.cursor()
        self.hill_cipher = HillCipher(fc.key_matriz())
        self.inicializar_interface()
        self.carregar_produtos()

        # Variáveis para armazenar os percentuais
        self.percentual_custo_fixo = None
        self.percentual_custo_operacional = None
        self.percentual_imposto = None
        self.percentual_comissao_venda = None
        self.percentual_margem_lucro = None
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
            self.root.withdraw()
            CalculadoraPrecoVenda(self.root, self.entry_preco_venda_principal, self, self.codigo,self.entry_custo_aquisicao)
    def carregar_produtos(self):
        # Método para carregar produtos do banco de dados e exibí-los na treeview
        self.tree.delete(*self.tree.get_children())  # Limpa a treeview
        sql = "SELECT codigo_de_barras, nome FROM tbl_produtos"
        self.cursor.execute(sql)
        produtos = self.cursor.fetchall()
        for produto in produtos:
            codigo, nome = produto  # dar valor
            nome = self.hill_cipher.decrypt(nome)  # decrypt nome
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
                # Descriptografa os campos
                nome = self.hill_cipher.decrypt(nome)
                descricao = self.hill_cipher.decrypt(descricao)
                fornecedor = self.hill_cipher.decrypt(fornecedor)
                
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
    def obter_fornecedores(self):
        # Função para obter a lista de fornecedores do banco de dados
        try:
            self.cursor.execute("SELECT nome FROM tbl_fornecedores")
            fornecedores = [row[0] for row in self.cursor.fetchall()]
            return fornecedores
        except oracledb.DatabaseError as e:
            messagebox.showerror("Erro", f"Erro ao acessar a lista de fornecedores: {e}")
            return []
    def atualizar_produto(self):
        # Método para atualizar os dados do produto no banco de dados
        if self.codigo:
            # Obtém os valores dos campos de entrada
            self.nome = self.entry_nome.get()
            self.descricao = self.entry_descricao.get()
            self.preco_de_compra = self.entry_custo_aquisicao.get()
            self.unidades = self.entry_unidades.get()
            self.fornecedor = self.combo_fornecedor.get()
            self.preco_de_venda = self.entry_preco_venda_principal.get()

            percentual_custo_fixo = self.percentual_custo_fixo
            percentual_custo_operacional = self.percentual_custo_operacional
            percentual_imposto = self.percentual_imposto
            percentual_comissao_venda = self.percentual_comissao_venda
            percentual_margem_lucro = self.percentual_margem_lucro
            
            # Validações dos campos
            if not fc.validar_nvarchar2(self.nome, 50, 1):
                return
            if not fc.validar_nvarchar2(self.descricao, 50, 0):
                return
            if not fc.validar_number("preço de venda", self.preco_de_venda, 1):
                return
            if not fc.validar_number("preço de compra", self.preco_de_compra, 1):
                return
            if not fc.validar_number("unidades", self.unidades, 1):
                return

            # Converte valores para tipos apropriados
            preco_de_venda = self.preco_de_venda.replace(',', '.')
            preco_de_venda = float(preco_de_venda)

            preco_de_compra = self.preco_de_compra.replace(',', '.')
            preco_de_compra = float(preco_de_compra)

            unidades = self.unidades.replace(',', '.')
            unidades = int(unidades)

            # Criptografa os campos
            nome = self.hill_cipher.encrypt(self.nome)
            descricao = self.hill_cipher.encrypt(self.descricao)
            fornecedor = self.hill_cipher.encrypt(self.fornecedor)
            
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

                # Atualiza os dados do produto na tabela tbl_produto_composicao
                sql_composicao = """
                UPDATE tbl_produto_composicao
                SET percentual_custo_fixo = :PERCENTUAL_CUSTO_FIXO, percentual_custo_operacional = :PERCENTUAL_CUSTO_OPERACIONAL,
                    percentual_imposto = :PERCENTUAL_IMPOSTO, percentual_comissao_venda = :PERCENTUAL_COMISSAO_VENDA,
                    percentual_margem_lucro = :PERCENTUAL_MARGEM_LUCRO
                WHERE codigo_de_barras = :CODIGO_DE_BARRAS
                """
                self.cursor.execute(sql_composicao, {
                    "PERCENTUAL_CUSTO_FIXO": percentual_custo_fixo,
                    "PERCENTUAL_CUSTO_OPERACIONAL": percentual_custo_operacional,
                    "PERCENTUAL_IMPOSTO": percentual_imposto,
                    "PERCENTUAL_COMISSAO_VENDA": percentual_comissao_venda,
                    "PERCENTUAL_MARGEM_LUCRO": percentual_margem_lucro,
                    "CODIGO_DE_BARRAS": self.codigo
                })
                
                self.connection.commit()
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso.")
                self.carregar_produtos()
                self.codigo = None
                self.root.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar o produto: {e}")
        else:
            messagebox.showerror("Erro", "Nenhum produto selecionado.")

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
        fornecedores = self.obter_fornecedores()
        self.combo_fornecedor = ctk.CTkComboBox(self.frame_editar, values=fornecedores)
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
            # Descriptografa os campos
            nome = self.hill_cipher.decrypt(nome)
            descricao = self.hill_cipher.decrypt(descricao)
            fornecedor = self.hill_cipher.decrypt(fornecedor)
            
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
