import tkinter as tk
from tkinter import ttk, messagebox
import oracledb

connection = oracledb.connect(user="SYSTEM", password="testador", host="localhost", port=1521)
cursor = connection.cursor()

class ExcluirProduto():
    def __init__(self, root_parameter):
        self.root = root_parameter
        self.root.title("Excluir Produto")
        self.excluir_design()
        self.carregar_produtos()
        self.root.mainloop()

    def carregar_produtos(self):
        sql = "SELECT codigo_de_barras, nome FROM tbl_produtos"
        cursor.execute(sql)
        produtos = cursor.fetchall()
        for produto in produtos:
            codigo, nome = produto
            self.tree.insert("", "end", values=(codigo, nome))

    def confirmar_exclusao(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showerror("Erro", "Selecione um produto para excluir.")
            return

        codigo = self.tree.item(item_selecionado, "values")[0]
        nome_produto = self.tree.item(item_selecionado, "values")[1]
        resposta = messagebox.askyesno("Confirmação", f"Você realmente deseja excluir o produto '{nome_produto}'?")

        if resposta:
            self.excluir_produto(codigo)

    def excluir_produto(self, codigo):
        sql = "DELETE FROM tbl_produtos WHERE codigo_de_barras = :CODIGO_DE_BARRAS"
        cursor.execute(sql, {"CODIGO_DE_BARRAS": codigo})
        connection.commit()
        messagebox.showinfo("Sucesso", "Produto excluído com sucesso.")
        self.tree.delete(*self.tree.get_children())  # Limpar a árvore
        self.carregar_produtos()  # Recarregar os produtos após a exclusão

    def excluir_design(self):
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        label_titulo = ttk.Label(frame, text="Lista de Produtos")
        label_titulo.pack()

        self.tree = ttk.Treeview(frame, columns=("Código de Barras", "Nome"), show="headings")
        self.tree.heading("Código de Barras", text="Código de Barras")
        self.tree.heading("Nome", text="Nome")
        self.tree.pack(fill=tk.BOTH, expand=True)

        button_excluir = ttk.Button(frame, text="Excluir Produto", command=self.confirmar_exclusao)
        button_excluir.pack()

if __name__ == "__main__":
    root = tk.Tk()
    ExcluirProduto(root)
