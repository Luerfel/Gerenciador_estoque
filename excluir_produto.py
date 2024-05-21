import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import oracledb
import fc

class ExcluirProduto():
    def __init__(self, root_parameter):
        # Inicializa a janela principal da aplicação
        self.root = root_parameter
        self.root.title("Excluir Produto")
        # Inicializa a conexão e o cursor do banco de dados
        self.connection = fc.conectar_banco()
        if self.connection:
            self.cursor = self.connection.cursor()
            # Chama o método para configurar o design da interface
            self.excluir_design()
            # Carrega os produtos na árvore
            self.carregar_produtos()
        else:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            self.root.destroy()
        # Mantém a aplicação em execução
        self.root.mainloop()

    def carregar_produtos(self):
        # Consulta o banco de dados para obter os produtos e carrega-os na árvore
        sql = "SELECT codigo_de_barras, nome FROM tbl_produtos"
        self.cursor.execute(sql)
        produtos = self.cursor.fetchall()
        for produto in produtos:
            self.codigo, nome = produto
            self.tree.insert("", "end", values=(self.codigo, nome))

    def confirmar_exclusao(self):
        # Confirma se um produto foi selecionado antes de excluir
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showerror("Erro", "Selecione um produto para excluir.")
            return

        # Obtém o código e o nome do produto selecionado
        codigo = self.tree.item(item_selecionado, "values")[0]
        nome_produto = self.tree.item(item_selecionado, "values")[1]
        # Exibe uma caixa de diálogo para confirmar a exclusão
        resposta = messagebox.askyesno("Confirmação", f"Você realmente deseja excluir o produto '{nome_produto}'?")

        if resposta:
            # Chama o método para excluir o produto do banco de dados
            self.excluir_produto(codigo)

    def excluir_produto(self, codigo):
        # Remove o produto do banco de dados
        sql = "DELETE FROM tbl_produto_composicao WHERE codigo_de_barras = :CODIGO_DE_BARRAS"
        self.cursor.execute(sql, {"CODIGO_DE_BARRAS": codigo})
        self.connection.commit()
        sql = "DELETE FROM tbl_produtos WHERE codigo_de_barras = :CODIGO_DE_BARRAS"
        self.cursor.execute(sql, {"CODIGO_DE_BARRAS": codigo})
        self.connection.commit()
        # Exibe uma mensagem de sucesso após a exclusão
        messagebox.showinfo("Sucesso", "Produto excluído com sucesso.")
        # Limpa a árvore e recarrega os produtos após a exclusão
        self.tree.delete(*self.tree.get_children())
        self.carregar_produtos()

    def buscar_produto(self):
        # Busca um produto pelo código
        codigo_busca = self.entry_codigo.get()
        sql = "SELECT codigo_de_barras, nome FROM tbl_produtos WHERE codigo_de_barras = :CODIGO_DE_BARRAS"
        self.cursor.execute(sql, {"CODIGO_DE_BARRAS": codigo_busca})
        produto = self.cursor.fetchone()
        if produto:
            self.codigo, self.nome = produto
            # Limpa a árvore e exibe o produto encontrado
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=(self.codigo, self.nome))
        else:
            # Exibe uma mensagem de erro se o produto não for encontrado
            messagebox.showerror("Erro", "Produto não encontrado.")

    def excluir_design(self):
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
        
        # Adiciona um botão para excluir produto
        button_excluir = ctk.CTkButton(frame_busca, text="Excluir Produto", command=self.confirmar_exclusao)
        button_excluir.grid(row=1, column=3, sticky=tk.W, padx=5)

if __name__ == "__main__":
    # Inicia a aplicação
    root = ctk.CTk()
    ExcluirProduto(root)
