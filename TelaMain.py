import tkinter as tk
import tkinter.messagebox as messagebox
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
        self.setup_bindings()
        self.root.protocol("WM_DELETE_WINDOW", self.confirm_exit)
        self.root.mainloop()

    def conectar_bd(self):
        """
        Conecta ao banco de dados Oracle.
        """
        try:
            self.connection = oracledb.connect(user="SYSTEM", password="senha", host="localhost", port=1521)
            self.cursor = self.connection.cursor()
            print("Conexão ao banco de dados realizada com sucesso.")
        except oracledb.DatabaseError as e:
            error, = e.args
            print(f"Erro ao conectar ao banco de dados: {error.message}")
            messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao banco de dados. Verifique suas credenciais e tente novamente.")
            self.root.destroy()

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

    def setup_bindings(self):
        """
        Configura os atalhos de teclado.
        """
        self.root.bind("<F1>", self.cadastrar_produto)
        self.root.bind("<F2>", self.consultar_produto)
        self.root.bind("<F3>", self.editar_produto)
        self.root.bind("<F4>", self.excluir_produto)
        self.root.bind("<F5>", self.cadastrar_fornecedor)
        self.root.bind("<F6>", self.cancelar_item)
        self.root.bind("<F7>", self.limpar_tela)

    def cancelar_item(self, event=None):
        """
        Cancela o item selecionado na Treeview.
        """
        if not self.tree.selection():
            messagebox.showwarning("Aviso", "Nenhum item selecionado para cancelar.")
            return
        item_selecionado = self.tree.selection()[0]
        self.tree.delete(item_selecionado)
        self.atualizar_valor_total()

    def buttons_design(self):
        """
        Cria e estiliza os botões na tela principal.
        """
        self.buttons_container = ctk.CTkFrame(self.root, fg_color="#242424")
        self.buttons_container.grid(row=0, column=0, columnspan=12, padx=20, pady=20, sticky="nsew")
        button_data = [
            ("F1\nCadastrar Produto", 0, 0, self.cadastrar_produto),
            ("F2\nConsultar Produto", 0, 1, self.consultar_produto),
            ("F3\nEditar Produto", 0, 2, self.editar_produto),
            ("F4\nExcluir Produto", 0, 3, self.excluir_produto),
            ("F5\nCadastrar Fornecedor", 0, 4, self.cadastrar_fornecedor),  
            ("F6\nCancelar Item", 0, 5, self.cancelar_item),
            ("F7\nCancelar Venda", 0, 6, self.limpar_tela),
            ("F8\nConcluir Venda", 0, 7, None)  # Função não implementada
        ]
        for text, row, column, command in button_data:
            button = ctk.CTkButton(self.buttons_container, text=text, width=80, height=40, corner_radius=13)
            button.grid(row=row, column=column, padx=10, pady=10)
            button.configure(hover_color="#5662f6", cursor="hand2")
            if command:
                button.bind("<Button-1>", command)

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
    def cadastrar_fornecedor(self, event=None):
        """
        Abre o arquivo de exclusão de produto.
        """
        subprocess.Popen(["python", "cadastrar_fornecedor.py"])


    def buscar_produto(self):
        """
        Busca um produto pelo código de barras.
        """
        termo_busca = self.entry_busca.get()
        try:
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
        except oracledb.DatabaseError as e:
            error, = e.args
            print(f"Erro ao buscar produto: {error.message}")
            messagebox.showerror("Erro de Banco de Dados", "Ocorreu um erro ao buscar o produto. Tente novamente.")

    def limpar_tela(self, event=None):
        """
        Limpa a tela e cancela a venda atual.
        """
        resposta = messagebox.askyesno("Cancelar Venda", "Tem certeza que deseja cancelar a venda atual? Todos os itens serão removidos.")
        if resposta:
            self.entry_busca.delete(0, ctk.END)
            self.nome_entry.delete(0, ctk.END)
            self.unitario_entry.delete(0, ctk.END)
            self.quantidade_entry.delete(0, ctk.END)
            self.total_entry.delete(0, ctk.END)
            self.tree.delete(*self.tree.get_children())
            self.label_total.configure(text="Valor Total : R$ 0.00")
            self.limpar_campos()

    def listar_produtos(self):
        """
        Exibe uma lista de produtos na tela principal com uma aparência aprimorada.
        """
        # configuração da tela
        style = ttk.Style()
        style.configure("Treeview",
                    background="#f0f0f0",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#f0f0f0",
                    font=("arial", 11))
        style.map('Treeview', background=[('selected', '#347083')])
    
        # Alternar as cores das linhas
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
   

        # Frame para conter a Treeview e a barra de rolagem
        tree_frame = ctk.CTkFrame(self.root)
        tree_frame.grid(row=1, column=1, padx=20, pady=20, sticky='nsew')
    
        # Barra de rolagem vertical
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        vsb.pack(side='right', fill='y')
    
    
        self.tree = ttk.Treeview(tree_frame, columns=('col2', 'col3', 'col4', 'col5'), show='headings',
                             height=20, yscrollcommand=vsb.set, style="Treeview")

    
        vsb.config(command=self.tree.yview)
    
        # Definindo as colunas
        self.tree.column('col2', minwidth=0, width=100, anchor='center')
        self.tree.column('col3', minwidth=0, width=150, anchor='center')
        self.tree.column('col4', minwidth=0, width=50, anchor='center')
        self.tree.column('col5', minwidth=0, width=100, anchor='center')
    
        # Definindo os cabeçalhos
        self.tree.heading('col2', text='Código de Barra')
        self.tree.heading('col3', text='Nome Produto')
        self.tree.heading('col4', text='Quantidade')
        self.tree.heading('col5', text='Valor Total')
    
        # Empacotando a Treeview
        self.tree.pack(fill='both', expand=True)
    
        # Estilo para alternar cores de linhas
        self.tree.tag_configure('evenrow', background="lightblue")

    def entry_info(self):
        """
        Cria e estiliza os campos de entrada de informações.
        """
        container = ctk.CTkFrame(self.root, fg_color="#242424", corner_radius=22)
        container.grid(row=1, column=0, padx=20, pady=10, sticky='w')

        label_busca = ctk.CTkLabel(container, text="Código de Barras", bg_color="#242424")
        label_busca.grid(row=0, column=0, padx=(10, 5), pady=5, sticky='w')
        self.entry_busca = ctk.CTkEntry(container, bg_color="#2b2b2b")
        self.entry_busca.grid(row=0, column=1, padx=(0, 10), pady=5, sticky='ew')

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

        adicionar_button = ctk.CTkButton(container, text="Adicionar Item", width=10, height=2, corner_radius=5, command=self.adicionar_produto)
        adicionar_button.grid(row=5, column=1, padx=(10, 0), pady=10, sticky='w')
        adicionar_button.configure(hover_color="#5662f6", cursor="hand2")

    def calcular_total(self, event=None):
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
        try:
            quantidade = int(self.quantidade_entry.get())
            valor_unitario = float(self.unitario_entry.get().replace("R$", "").replace(",", "."))
            valor_total = quantidade * valor_unitario
            self.tree.insert('', 'end', values=(codigo, nome, quantidade, f"R$ {valor_total:.2f}"))
            self.atualizar_valor_total()
            self.limpar_campos()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores válidos.")

    def limpar_campos(self):
        """
        Limpa os campos de entrada.
        """
        self.entry_busca.delete(0, tk.END)
        self.nome_entry.configure(state=tk.NORMAL)
        self.unitario_entry.configure(state=tk.NORMAL)
        self.total_entry.configure(state=tk.NORMAL)
        self.nome_entry.delete(0, tk.END)
        self.unitario_entry.delete(0, tk.END)
        self.quantidade_entry.delete(0, tk.END)
        self.total_entry.delete(0, tk.END)
        self.nome_entry.configure(state='readonly')
        self.unitario_entry.configure(state='readonly')
        self.total_entry.configure(state='readonly')

    def criar_label_total(self):
        """
        Cria uma label para mostrar o valor total de todos os itens.
        """
        self.label_total = ctk.CTkLabel(self.root, text="Valor Total : R$ 0.00", font=("Helvetica", 30))
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
            self.connection.close()
            self.root.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    MainScreen(root)
