import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import oracledb
from calculo_venda import CalculadoraPrecoVenda

# Estabelece a conexão com o banco de dados Oracle.
connection = oracledb.connect(user="SYSTEM", password="senha", host="localhost", port=1521)
cursor = connection.cursor()

class editar_produto():
    def __init__(self, root_parameter):
        self.root = root_parameter
        self.root.title("Editar Produto")
        self.root.resizable(False, False)
        self.codigo = None  # Armazena o código do produto que está sendo editado
        self.editar_design()
        self.carregar_produtos()
        self.root.mainloop()

    def acessar_calculadora_preco_venda(self):
        self.root.withdraw()
        calculadora = CalculadoraPrecoVenda(self.root, self.entry_preco_venda_principal)

    def carregar_produtos(self):
        sql = "SELECT codigo_de_barras, nome FROM tbl_produtos"
        cursor.execute(sql)
        produtos = cursor.fetchall()
        for produto in produtos:
            codigo, nome = produto
            self.tree.insert("", "end", values=(codigo, nome))

    def editar_produto_design(self):
        frame = ctk.CTkFrame(self.root)
        frame.place(relwidth=1, relheight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=3)

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
        self.combo_fornecedor = ctk.CTkComboBox(frame, state="readonly", values=["Fornecedor 1", "Fornecedor 2", "Fornecedor 3"])
        self.combo_fornecedor.grid(row=4, column=1, sticky=tk.EW, pady=5, padx=15)

        label_preco_venda_principal = ctk.CTkLabel(frame, text="Preço de Venda:")
        label_preco_venda_principal.grid(row=5, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_preco_venda_principal = ctk.CTkEntry(frame)
        self.entry_preco_venda_principal.grid(row=5, column=1, sticky=tk.EW, pady=5, padx=15)

        botao_calcular_preco = ctk.CTkButton(frame, text="Calcular Preço de Venda", command=self.acessar_calculadora_preco_venda)
        botao_calcular_preco.grid(row=5, column=2, padx=5, pady=5)

        buttons_frame = ctk.CTkFrame(frame, fg_color="#2b2b2b")
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        buttons_frame.grid(row=6, column=0, columnspan=3, pady=4)

        button_atualizar = ctk.CTkButton(buttons_frame, text="Atualizar Produto", command=self.atualizar_produto)
        button_atualizar.grid(row=0, column=0, padx=5, sticky=tk.W)


    def buscar_produto(self):
        codigo_busca = self.entry_codigo.get()
        sql = "SELECT codigo_de_barras, nome, descricao, custo_aquisicao, unidades, fornecedor, preco_venda FROM tbl_produtos WHERE codigo_de_barras = :CODIGO_DE_BARRAS"
        cursor.execute(sql, {"CODIGO_DE_BARRAS": codigo_busca})
        produto = cursor.fetchone()
        if produto:
            self.codigo, nome, descricao, custo_aquisicao, unidades, fornecedor, preco_venda = produto
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, nome)
            self.entry_descricao.delete(0, tk.END)
            self.entry_descricao.insert(0, descricao)
            self.entry_custo_aquisicao.delete(0, tk.END)
            self.entry_custo_aquisicao.insert(0, custo_aquisicao)
            self.entry_unidades.delete(0, tk.END)
            self.entry_unidades.insert(0, unidades)
            self.combo_fornecedor.set(fornecedor)
            self.entry_preco_venda_principal.delete(0, tk.END)
            self.entry_preco_venda_principal.insert(0, preco_venda)
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=(self.codigo, nome))
        else:
            messagebox.showerror("Erro", "Produto não encontrado.")

    def atualizar_produto(self):
        if self.codigo:
            nome = self.entry_nome.get()
            descricao = self.entry_descricao.get()
            custo_aquisicao = self.entry_custo_aquisicao.get()
            unidades = self.entry_unidades.get()
            fornecedor = self.combo_fornecedor.get()
            preco_venda = self.entry_preco_venda_principal.get()
            sql = """
            UPDATE tbl_produtos
            SET nome = :NOME, descricao = :DESCRICAO, custo_aquisicao = :CUSTO_AQUISICAO, unidades = :UNIDADES,
                fornecedor = :FORNECEDOR, preco_venda = :PRECO_VENDA
            WHERE codigo_de_barras = :CODIGO_DE_BARRAS
            """
            cursor.execute(sql, {
                "NOME": nome,
                "DESCRICAO": descricao,
                "CUSTO_AQUISICAO": custo_aquisicao,
                "UNIDADES": unidades,
                "FORNECEDOR": fornecedor,
                "PRECO_VENDA": preco_venda,
                "CODIGO_DE_BARRAS": self.codigo
            })
            connection.commit()
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso.")
        else:
            messagebox.showerror("Erro", "Nenhum produto selecionado para edição.")

    def editar_design(self):
        self.frame = ctk.CTkFrame(self.root)
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        label_titulo = ctk.CTkLabel(self.frame, text="Lista de Produtos", text_color="#f9f6ee")
        label_titulo.grid(row=0, column=0, sticky=tk.W)

        self.tree = ttk.Treeview(self.frame, columns=("Código de Barras", "Nome"), show="headings")
        self.tree.column("0", minwidth=0, width=280)
        self.tree.column("1", minwidth=0, width=280)
        self.tree.heading("Código de Barras", text="Código de Barras")
        self.tree.heading("Nome", text="Nome")
        self.tree.grid(row=0, column=0, sticky=tk.W)

        frame_busca = ctk.CTkFrame(self.frame, fg_color="#2b2b2b")
        frame_busca.place(relwidth=1, relheight=1)
        frame_busca.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame_busca.columnconfigure(0, weight=1)

        label_codigo = ctk.CTkLabel(frame_busca, text="Código do Produto:", fg_color="#2b2b2b")
        label_codigo.grid(row=1, columnspan=2, sticky=tk.W, padx=3)
        self.entry_codigo = ctk.CTkEntry(frame_busca)
        self.entry_codigo.grid(row=1, column=1, sticky=tk.W)

        button_buscar = ctk.CTkButton(frame_busca, text="Buscar Produto", command=self.buscar_produto)
        button_buscar.grid(row=1, column=2, sticky=tk.W, padx=5)

        button_editar = ctk.CTkButton(frame_busca, text="Editar Produto", command=self.editar_produto_design)
        button_editar.grid(row=1, column=3, sticky=tk.W, padx=5)

if __name__ == "__main__":
    root = ctk.CTk()
    editar_produto(root)
