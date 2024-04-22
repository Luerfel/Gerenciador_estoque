import tkinter as tk
from tkinter import ttk, messagebox
import oracledb

connection = oracledb.connect(user="SYSTEM", password="senha", host="localhost", port=1521)
cursor = connection.cursor()

class EditarProduto():
    def __init__(self, root_parameter):
        self.root = root_parameter
        self.root.title("Editar Produto")
        self.codigo_de_barras = None  # Variável global para armazenar o código de barras
        self.editar_design()
        self.root.mainloop()

    def fechar_janela_editar_produto(self):
        self.root.deiconify()
        self.nova_janela.destroy()

    def consultar_banco_de_dados(self, codigo):
        sql = """
            SELECT COUNT(*) FROM tbl_produtos WHERE codigo_de_barras = :CODIGO_DE_BARRAS
            """
        cursor.execute(sql, {"CODIGO_DE_BARRAS": codigo})
        resultado = cursor.fetchone()[0]
        # se o resultado for maior que 1 então significa que existe
        if resultado != 1:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return
        
        sql = """
        SELECT nome, descricao, preco_de_compra, preco_de_venda, unidades, fornecedor 
        FROM tbl_produtos WHERE codigo_de_barras = :CODIGO_DE_BARRAS 
        """
        cursor.execute(sql, {"CODIGO_DE_BARRAS": codigo})
        produto = cursor.fetchone()  # Obter o produto da consulta
        if produto:
            self.editar_produto()  # Chamar o método para editar o produto
            # Preencher os campos na interface gráfica com os dados do produto
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
        self.codigo_de_barras = self.entry_codigo_de_barras.get()

        if not self.codigo_de_barras:
            messagebox.showerror("Erro", "Código de barras inválido.")
            return

        self.consultar_banco_de_dados(self.codigo_de_barras)

    def atualizar_produto(self):
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
        # Crie uma nova janela
        self.root.iconify()
        self.nova_janela = tk.Toplevel(self.root)
        self.nova_janela.title("Editar Produto")
        self.nova_janela.protocol("WM_DELETE_WINDOW", self.fechar_janela_editar_produto)

        # Adicione conteúdo à nova janela
        frame = ttk.Frame(self.nova_janela, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        label_nome = ttk.Label(frame, text="Nome:")
        label_nome.grid(row=0, column=0, sticky=tk.W)
        self.entry_nome = ttk.Entry(frame, width=50)
        self.entry_nome.grid(row=0, column=1, sticky=tk.W)

        label_descricao = ttk.Label(frame, text="Descrição:")
        label_descricao.grid(row=1, column=0, sticky=tk.W)
        self.entry_descricao = ttk.Entry(frame, width=50)
        self.entry_descricao.grid(row=1, column=1, sticky=tk.W)

        label_custo_aquisicao = ttk.Label(frame, text="Custo de Aquisição:")
        label_custo_aquisicao.grid(row=2, column=0, sticky=tk.W)
        self.entry_custo_aquisicao = ttk.Entry(frame, width=50)
        self.entry_custo_aquisicao.grid(row=2, column=1, sticky=tk.W)

        label_unidades = ttk.Label(frame, text="Unidades:")
        label_unidades.grid(row=3, column=0, sticky=tk.W)
        self.entry_unidades = ttk.Entry(frame, width=50)
        self.entry_unidades.grid(row=3, column=1, sticky=tk.W)

        label_fornecedor = ttk.Label(frame, text="Fornecedor:")
        label_fornecedor.grid(row=4, column=0, sticky=tk.W)
        self.combo_fornecedor = ttk.Combobox(frame, width=47, state="readonly")
        self.combo_fornecedor['values'] = ("Fornecedor 1", "Fornecedor 2", "Fornecedor 3")  # Adicione os fornecedores
        self.combo_fornecedor.grid(row=4, column=1, sticky=tk.W)

        label_preco_venda_principal = ttk.Label(frame, text="Preço de Venda:")
        label_preco_venda_principal.grid(row=5, column=0, sticky=tk.W)
        self.entry_preco_venda_principal = ttk.Entry(frame, width=50)
        self.entry_preco_venda_principal.grid(row=5, column=1, sticky=tk.W)

        # Botão para atualizar o produto
        button_atualizar = ttk.Button(frame, text="Atualizar Produto", command=self.atualizar_produto)
        button_atualizar.grid(row=6, column=0, columnspan=2, pady=10)

    def editar_design(self):
        frame = ttk.Frame(self.root, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Campos de entrada
        label_codigo_de_barras = ttk.Label(frame, text="Digite o código de barras do produto:")
        label_codigo_de_barras.grid(row=0, column=0, sticky=tk.W)
        self.entry_codigo_de_barras = ttk.Entry(frame, width=50)
        self.entry_codigo_de_barras.grid(row=0, column=1, sticky=tk.W)

        # Botão para encontrar produto
        button_encontrar_produto = ttk.Button(frame, text="Procurar Produto", command=self.selecionar_produto)
        button_encontrar_produto.grid(row=1, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    EditarProduto(root)
