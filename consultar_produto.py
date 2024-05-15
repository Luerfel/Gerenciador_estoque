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

class ConsultarProduto():
    def __init__(self, root_parameter):
        self.root = root_parameter
        self.root.title("Consultar Produto")
        self.consultar_design()
        self.carregar_produtos()
        self.root.mainloop()

    def carregar_produtos(self):
        sql = "SELECT codigo_de_barras, nome, descricao, preco_de_compra, preco_de_venda, fornecedor FROM tbl_produtos"
        cursor.execute(sql)
        produtos = cursor.fetchall()
        for produto in produtos:
            codigo, nome, descricao, preco_de_compra, preco_de_venda, fornecedor = produto
            self.tree.insert("", "end", values=(codigo, nome, descricao, preco_de_compra, preco_de_venda, fornecedor))

    def buscar_produto(self):
        termo_busca = self.entry_busca.get()
        tipo_busca = self.combo_tipo_busca.get()
        if tipo_busca == "Código de Barras":
            sql = "SELECT codigo_de_barras, nome, descricao, preco_de_compra, preco_de_venda, fornecedor FROM tbl_produtos WHERE codigo_de_barras = :TERMOS_BUSCA"
        else:  # Buscar por nome
            sql = "SELECT codigo_de_barras, nome, descricao, preco_de_compra, preco_de_venda, fornecedor FROM tbl_produtos WHERE nome LIKE :TERMOS_BUSCA"
        cursor.execute(sql, {"TERMOS_BUSCA": termo_busca})
        resultados = cursor.fetchall()
        if resultados:
            self.tree.delete(*self.tree.get_children())  # Limpar a árvore
            for produto in resultados:
                codigo, nome, descricao, preco_de_compra, preco_de_venda, fornecedor = produto
                self.tree.insert("", "end", values=(codigo, nome, descricao, preco_de_compra, preco_de_venda, fornecedor))
        else:
            messagebox.showerror("Erro", "Nenhum resultado encontrado.")

    def consultar_design(self):
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        label_titulo = ttk.Label(frame, text="Consulta de Produtos")
        label_titulo.pack()

        frame_busca = ttk.Frame(frame)
        frame_busca.pack(fill=tk.X)

        label_busca = ttk.Label(frame_busca, text="Buscar Produto:")
        label_busca.pack(side=tk.LEFT)

        self.entry_busca = ttk.Entry(frame_busca)
        self.entry_busca.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.combo_tipo_busca = ttk.Combobox(frame_busca, values=["Código de Barras", "Nome"], state="readonly")
        self.combo_tipo_busca.pack(side=tk.LEFT)
        self.combo_tipo_busca.current(0)  # Definir o valor padrão como "Código de Barras"

        button_buscar = ttk.Button(frame_busca, text="Buscar", command=self.buscar_produto)
        button_buscar.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(frame, columns=("Código de Barras", "Nome", "Descrição", "Preço Compra", "Preço Venda", "Fornecedor"), show="headings")
        self.tree.heading("Código de Barras", text="Código de Barras")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Descrição", text="Descrição")
        self.tree.heading("Preço Compra", text="Preço Compra")
        self.tree.heading("Preço Venda", text="Preço Venda")
        self.tree.heading("Fornecedor", text="Fornecedor")
        self.tree.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    ConsultarProduto(root)
