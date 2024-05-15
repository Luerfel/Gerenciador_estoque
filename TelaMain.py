import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter.ttk import Treeview
from tkinter import ttk
import customtkinter as ctk
import oracledb
import subprocess

class MainScreen:
    """
    Classe para a tela principal do sistema de gerenciamento de estoque.
    """

    def __init__(self, root_parameter):
        """
        Inicializa a tela principal.

        Args:
            root_parameter (tk.Tk): A janela principal do aplicativo.
        """
        self.root = root_parameter
        self.conectar_bd()
        self.montar_tela_principal()
        self.ajustar_grid()
        self.buttons_design()
        self.listar_produtos()
        self.entry_info()
        self.criar_label_total()
        self.root.protocol("WM_DELETE_WINDOW", self.confirm_exit)
        self.root.bind("<F1>", self.cadastrar_produto)
        self.root.bind("<F2>", self.consultar_produto)
        self.root.bind("<F3>", self.editar_produto)
        self.root.bind("<F4>", self.excluir_produto)
        self.root.bind("<F6>", self.cancelar_item)
        self.root.bind("<F7>", self.limpar_tela)

        self.root.mainloop()

    def conectar_bd(self):
        """
        Conecta ao banco de dados Oracle.
        """
        self.connection = oracledb.connect(user="SYSTEM", password="senha", host="localhost", port=1521)
        self.cursor = self.connection.cursor()

    def ajustar_grid(self):
        """
        Ajusta a configuração da grade da janela principal.
        """
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=6)
        self.root.grid_rowconfigure(2, weight=6)
        self.root.grid_columnconfigure(0, weight=6)
        self.root.grid_columnconfigure(1, weight=3)

    def montar_tela_principal(self):
        """
        Configura a aparência da tela principal.
        """
        self.root.geometry("1200x720")
        self.root.title("Stock Management System")
        self.root.resizable(False, False)
        self.root.configure(background="#f9f6ee")

    def cancelar_item(self, event=None):
        # Verifica se algum item está selecionado
        if not self.tree.selection():
            messagebox.showwarning("Aviso", "Nenhum item selecionado para cancelar.")
            return

        # Obtém o item selecionado
        item_selecionado = self.tree.selection()[0]

        # Remove o item selecionado da Treeview
        self.tree.delete(item_selecionado)

        # Atualiza o valor total após cancelar o item
        self.atualizar_valor_total()

    def buttons_design(self):
        """
        Cria e estiliza os botões na tela principal.
        """
        self.buttons_container = ctk.CTkFrame(self.root, fg_color="#242424")
        self.buttons_container.grid(row=0, column=0, columnspan=12, padx=20, pady=20, sticky="nsew")
        button_data = [
            ("F1\nCadastrar Produto", 0, 0),
            ("F2\nConsultar Produto", 0, 1),
            ("F3\nEditar Produto", 0, 2),
            ("F4\nExcluir Produto", 0, 3),
            ("F5\nCadastrar Fornecedor", 0, 4),
            ("F6\nCancelar Item", 0, 5),
            ("F7\nCancelar Venda", 0,6),
            ("F8\nConcluir Venda", 0, 7)
        ]
        for text, row, column in button_data:
            button = ctk.CTkButton(self.buttons_container, text=text, width=80, height=40, corner_radius=13)
            button.grid(row=row, column=column, padx=10, pady=10)
            button.configure(hover_color="#5662f6", cursor="hand2")
            if text.startswith("F1"):
                button.bind("<Button-1>", self.cadastrar_produto)
            elif text.startswith("F2"):
                button.bind("<Button-1>", self.consultar_produto)
            elif text.startswith("F3"):
                button.bind("<Button-1>", self.editar_produto)
            elif text.startswith("F4"):
                button.bind("<Button-1>", self.excluir_produto)
            elif text.startswith("F6"):
                button.bind("<Button-1>", self.cancelar_item)
            elif text.startswith("F7"):
                button.bind("<Button-1>", self.limpar_tela)

    def cadastrar_produto(self, event=None):
        """
        Abre o arquivo de cadastro de produto.
        """
        subprocess.Popen(["python", "cadastrar_produto.py"])

    def consultar_produto(self, event=None):
        """
        Abre o arquivo de consulta de produto.
        """
        subprocess.Popen(["python", "consultar_produto.py"])

    def editar_produto(self, event=None):
        """
        Abre o arquivo de edição de produto.
        """
        subprocess.Popen(["python", "editar_produto.py"])

    def excluir_produto(self, event=None):
        """
        Abre o arquivo de exclusão de produto.
        """
        subprocess.Popen(["python", "excluir_produto.py"])
    def buscar_produto(self):
        termo_busca = self.entry_busca.get()
        sql = "SELECT nome, preco_de_venda FROM tbl_produtos WHERE codigo_de_barras = :TERMOS_BUSCA"
        self.cursor.execute(sql, {"TERMOS_BUSCA": termo_busca})
        resultado = self.cursor.fetchone()
        if resultado:
            nome, preco_venda = resultado
            self.nome_entry.configure(state=tk.NORMAL)
            self.unitario_entry.configure(state=tk.NORMAL)
            self.nome_entry.delete(0, tk.END)
            self.nome_entry.insert(0, nome)
            self.unitario_entry.delete(0, tk.END)
            self.unitario_entry.insert(0, f"R$ {preco_venda:.2f}")
            self.nome_entry.configure(state='readonly')
            self.unitario_entry.configure(state='readonly')
            self.quantidade_entry.delete(0, tk.END)
            self.quantidade_entry.insert(0, "1")
            self.calcular_total(None)
        else:
            messagebox.showerror("Erro", "Produto não encontrado.")

    def limpar_tela(self, event=None):
        # Exibe uma caixa de diálogo de confirmação
        resposta = messagebox.askyesno("Cancelar Venda", "Tem certeza que deseja cancelar a venda atual? Todos os itens serão removidos.")

        # Verifica se o usuário confirmou
        if resposta:
            # Limpa todos os campos
            self.entry_busca.delete(0, tk.END)
            self.nome_entry.delete(0, tk.END)
            self.unitario_entry.delete(0, tk.END)
            self.quantidade_entry.delete(0, tk.END)
            self.total_entry.delete(0, tk.END)

            # Redefine outros elementos da interface
            self.tree.delete(*self.tree.get_children())  # Limpa a lista de produtos
            self.label_total.configure(text="Valor Total : R$ 0.00")  # Redefine o valor total

    def listar_produtos(self):
        """
        Exibe uma lista de produtos na tela principal.
        """
        self.tree = ttk.Treeview(self.root, columns=('col2', 'col3', 'col4', 'col5'), show='headings', height=20)
        self.tree.column('#0', minwidth=0, width=0)
        self.tree.column('col2', minwidth=0, width=100)
        self.tree.column('col3', minwidth=0, width=100)
        self.tree.column('col4', minwidth=0, width=100)
        self.tree.column('col5', minwidth=0, width=100)
        self.tree.heading('#0', text='')
        self.tree.heading('col2', text='Código Produto')
        self.tree.heading('col3', text='Nome Produto')
        self.tree.heading('col4', text='Quantidade')
        self.tree.heading('col5', text='Valor Total')
        self.tree.grid(row=1, column=1)

    def entry_info(self):
        """
        Cria e estiliza os campos de entrada de informações.
        """
        container = ctk.CTkFrame(self.root, fg_color="#242424", corner_radius=22)
        container.grid(row=1, column=0, padx=20, pady=10, sticky='w')

        # Campo de busca (Código de Barras)
        label_busca = ctk.CTkLabel(container, text="Código de Barras", bg_color="#242424")
        label_busca.grid(row=0, column=0, padx=(10, 5), pady=5, sticky='w')
        self.entry_busca = ctk.CTkEntry(container, bg_color="#2b2b2b")
        self.entry_busca.grid(row=0, column=1, padx=(0, 10), pady=5, sticky='ew')

        # Botão de busca
        busca_button = ctk.CTkButton(container, text="Buscar", width=10, height=2, corner_radius=5, command=self.buscar_produto)
        busca_button.grid(row=0, column=2, padx=(10, 0), pady=10, sticky='w')
        busca_button.configure(hover_color="#5662f6", cursor="hand2")

        entry_data = [
            ("Nome", 1),
            ("Unitário R$", 2),
            ("Quantidade Total", 3),
            ("Total do Item R$", 4),
        ]

        for label_text, row in entry_data:
            label = ctk.CTkLabel(container, text=label_text, bg_color="#242424")
            label.grid(row=row, column=0, padx=(10, 5), pady=5, sticky='w')
            entry = ctk.CTkEntry(container, bg_color="#2b2b2b")
            entry.grid(row=row, column=1, padx=(0, 10), pady=5, sticky='ew')

            if label_text == "Nome":
                self.nome_entry = entry
                self.nome_entry.configure(state='readonly')
            elif label_text == "Unitário R$":
                self.unitario_entry = entry
                self.unitario_entry.configure(state='readonly')
            elif label_text == "Quantidade Total":
                self.quantidade_entry = entry
                self.quantidade_entry.bind("<FocusOut>", self.calcular_total)
                self.quantidade_entry.bind("<KeyRelease>", self.calcular_total)
            elif label_text == "Total do Item R$":
                self.total_entry = entry
                self.total_entry.configure(state='readonly')

        # Botão de adicionar produto à lista
        adicionar_button = ctk.CTkButton(container, text="Adicionar Item", width=10, height=2, corner_radius=5, command=self.adicionar_produto)
        adicionar_button.grid(row=5, column=1, padx=(10, 0), pady=10, sticky='w')
        adicionar_button.configure(hover_color="#5662f6", cursor="hand2")

    def calcular_total(self, event):
        """
        Calcula o total multiplicando o preço unitário pela quantidade total.
        """
        try:
            preco_unitario = float(self.unitario_entry.get().replace("R$", "").replace(",", "."))
            quantidade_total = float(self.quantidade_entry.get())
            total = preco_unitario * quantidade_total
            self.total_entry.configure(state=tk.NORMAL)
            self.total_entry.delete(0, tk.END)
            self.total_entry.insert(0, f"R$ {total:.2f}")
            self.total_entry.configure(state='readonly')
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido para quantidade ou preço unitário.")

    def adicionar_produto(self):
        """
        Adiciona um produto à lista de produtos.
        """
        codigo = self.entry_busca.get()
        if not codigo:
            messagebox.showerror("Erro", "Por favor, insira um código de barras válido.")
            return
    
        nome = self.nome_entry.get()
        if not nome:
            messagebox.showerror("Erro", "Por favor, busque um produto antes de adicioná-lo à lista.")
            return
    
        quantidade = int(self.quantidade_entry.get())
        valor_unitario = float(self.unitario_entry.get().replace("R$", "").replace(",", "."))
        valor_total = quantidade * valor_unitario
    
        self.tree.insert('', 'end', values=(codigo, nome, quantidade, f"R$ {valor_total:.2f}"))
        self.atualizar_valor_total()

        # Limpar os campos após adicionar o produto
        self.entry_busca.delete(0, tk.END)
    
        # Remover a configuração de somente leitura temporariamente
        self.nome_entry.configure(state=tk.NORMAL)
        self.unitario_entry.configure(state=tk.NORMAL)
        self.total_entry.configure(state=tk.NORMAL)
    
        self.nome_entry.delete(0, tk.END)
        self.unitario_entry.delete(0, tk.END)
        self.quantidade_entry.delete(0, tk.END)
        self.total_entry.delete(0, tk.END)
    
        # Restaurar a configuração de somente leitura
        self.nome_entry.configure(state='readonly')
        self.unitario_entry.configure(state='readonly')
        self.total_entry.configure(state='readonly')


    def criar_label_total(self):
        """
        Cria uma label para mostrar o valor total de todos os itens.
        """
        self.label_total = ctk.CTkLabel(self.root, text="Valor Total : R$ 0.00",font=("Helvetica", 30))
        self.label_total.grid(row=2, column=1, padx=20, pady=10, sticky='w')

    def atualizar_valor_total(self):
        """
        Atualiza o valor total de todos os itens.
        """
        total = 0
        for child in self.tree.get_children():
            total += float(self.tree.item(child, 'values')[3].replace("R$", "").replace(",", ""))
        self.label_total.configure(text=f"Valor Total : R$ {total:.2f}")

    def confirm_exit(self):
        """
        Exibe uma mensagem de confirmação ao sair do programa.
        """
        if messagebox.askokcancel("Sair", "Você tem certeza que deseja sair?"):
            self.root.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    MainScreen(root)
