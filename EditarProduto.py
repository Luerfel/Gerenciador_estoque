import tkinter as tk
import fc
from tkinter import ttk
from tkinter import messagebox
from tkinter import StringVar
import random
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

connection = oracledb.connect(user="SYSTEM", password="testador", host="localhost", port=1521)
cursor = connection.cursor()

class EditarProduto():
    def __init__(self, root_parameter):
        self.root = root_parameter
        self.root.title("Editar Produto")
        self.editar_design()
        self.root.mainloop()

    def fechar_janela_editar_produto(self):
        self.root.deiconify()
        self.nova_janela.destroy()

    def selecionar_produto(self):
        self.codigo_de_barra = self.entry_codigo_de_barra.get()

        if not fc.validar_nvarchar2(self.codigo_de_barra, 13, 0):
            messagebox.showerror("Erro", "Código de barras inválido.")
            return

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
        entry_nome = ttk.Entry(frame, width=50)
        entry_nome.grid(row=0, column=1, sticky=tk.W)

        label_descricao = ttk.Label(frame, text="Descrição:")
        label_descricao.grid(row=1, column=0, sticky=tk.W)
        entry_descricao = ttk.Entry(frame, width=50)
        entry_descricao.grid(row=1, column=1, sticky=tk.W)

        label_custo_aquisicao = ttk.Label(frame, text="Custo de Aquisição:")
        label_custo_aquisicao.grid(row=2, column=0, sticky=tk.W)
        entry_custo_aquisicao = ttk.Entry(frame, width=50)
        entry_custo_aquisicao.grid(row=2, column=1, sticky=tk.W)

        label_unidades = ttk.Label(frame, text="Unidades:")
        label_unidades.grid(row=3, column=0, sticky=tk.W)
        entry_unidades = ttk.Entry(frame, width=50)
        entry_unidades.grid(row=3, column=1, sticky=tk.W)

        label_fornecedor = ttk.Label(frame, text="Fornecedor:")
        label_fornecedor.grid(row=4, column=0, sticky=tk.W)
        combo_fornecedor = ttk.Combobox(frame, width=47, state="readonly")
        combo_fornecedor['values'] = ("Fornecedor 1", "Fornecedor 2", "Fornecedor 3")  # Aqui você pode adicionar os fornecedores cadastrados
        combo_fornecedor.grid(row=4, column=1, sticky=tk.W)

        label_preco_venda_principal = ttk.Label(frame, text="Preço de Venda:")
        label_preco_venda_principal.grid(row=5, column=0, sticky=tk.W)
        entry_preco_venda_principal = ttk.Entry(frame, width=50)
        entry_preco_venda_principal.grid(row=5, column=1, sticky=tk.W)


    def consultar_banco_de_dados(self, codigo):
        sql = """
        SELECT nome,descricao,preco_de_compra,preco_de_venda,unidades,fornecedor FROM tbl_produtos WHERE codigo_de_barra = 
        """
        cursor.execute(sql, {"CODIGO_DE_BARRAS": codigo})



    def editar_design(self):
        frame = ttk.Frame(self.root, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Campos de entrada
        label_codigo_de_barra = ttk.Label(frame, text="Digite o codigo de barras do produto:")
        label_codigo_de_barra.grid(row=0, column=0, sticky=tk.W)
        entry_codigo_de_barra = ttk.Entry(frame, width=50)
        entry_codigo_de_barra.grid(row=0, column=1, sticky=tk.W)

         # Botão para encontrar produto
        button_encontrar_produto = ttk.Button(frame, text="Procurar Produto", command=self.editar_produto)
        button_encontrar_produto.grid(row=6, column=0, columnspan=2, pady=10)


        

if __name__ == "__main__":
    root = tk.Tk()
    EditarProduto(root)