import customtkinter as ctk
from tkinter import messagebox
from tkinter.ttk import Treeview
from tkinter import ttk
from commons import Commons


class MainScreen(Commons):
    def __init__(self, root_parameter):
        self.root = root_parameter
        self.montar_tela_principal()
        self.design()
        self.ajustar_grid()
        self.buttons_design()
        self.listar_produtos()
        self.entry_info()
        self.root.protocol("WM_DELETE_WINDOW", self.confirm_exit)
        self.root.mainloop()

    def ajustar_grid(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=6)
        self.root.grid_rowconfigure(2, weight=6)
        self.root.grid_columnconfigure(0, weight=6)
        self.root.grid_columnconfigure(1, weight=3)


    def montar_tela_principal(self):
        self.root.geometry("1200x720")
        self.root.title("Stock Management System")
        self.root.resizable(False, False)
        self.root.configure(background="#f9f6ee")

    def buttons_design(self):
        self.buttons_container = ctk.CTkFrame(self.root, fg_color="#242424")
        self.buttons_container.grid(row=0, column=0, columnspan=12, padx=20, pady=20, sticky="nsew")
        consultar_button = ctk.CTkButton(self.buttons_container, text="F1\nConsultar", width=80, height=40, corner_radius=13)
        consultar_button.grid(row=0, column=0, padx=10, pady=10)
        consultar_button.configure(hover_color="#5662f6", cursor="hand2")
        nova_venda_button = ctk.CTkButton(self.buttons_container, text="F2\nNova Venda", width=80, height=40, corner_radius=13)
        nova_venda_button.grid(row=0, column=1, padx=10, pady=10)
        nova_venda_button.configure(hover_color="#5662f6", cursor="hand2")
        total_item_button = ctk.CTkButton(self.buttons_container, text="F3\nTotal do Item", width=80, height=40, corner_radius=13)
        total_item_button.grid(row=0, column=2, padx=10, pady=10)
        total_item_button.configure(hover_color="#5662f6", cursor="hand2")
        tabela_precos_button = ctk.CTkButton(self.buttons_container, text="F4\nTabela de preços", width=80, height=40,corner_radius=13)
        tabela_precos_button.grid(row=0, column=3, padx=10, pady=10)
        tabela_precos_button.configure(hover_color="#5662f6", cursor="hand2")
        quantidade_button = ctk.CTkButton(self.buttons_container, text="F5\nQuantidade", width=80, height=40, corner_radius=13)
        quantidade_button.grid(row=0, column=4, padx=10, pady=10)
        quantidade_button.configure(hover_color="#5662f6", cursor="hand2")
        valor_button = ctk.CTkButton(self.buttons_container, text="F6\nValor", width=80, height=40, corner_radius=13)
        valor_button.grid(row=0, column=5, padx=10, pady=10)
        valor_button.configure(hover_color="#5662f6", cursor="hand2")
        cancelar_item_button = ctk.CTkButton(self.buttons_container, text="F7\nCancelar Item", width=80, height=40, corner_radius=13)
        cancelar_item_button.grid(row=0, column=6, padx=10, pady=10)
        cancelar_item_button.configure(hover_color="#5662f6", cursor="hand2")
        excluir_venda_button = ctk.CTkButton(self.buttons_container, text="F8\nExcluir Venda", width=80, height=40, corner_radius=13)
        excluir_venda_button.grid(row=0, column=7, padx=10, pady=10)
        excluir_venda_button.configure(hover_color="#5662f6", cursor="hand2")

    def listar_produtos(self):
        tree = Treeview(self.root, columns=('col2', 'col3', 'col4', 'col5'), show='headings',height=20)
        tree.column('#0', minwidth=0, width=0)
        tree.column('col2', minwidth=0, width=100)
        tree.column('col3', minwidth=0, width=100)
        tree.column('col4', minwidth=0, width=100)
        tree.column('col5', minwidth=0, width=100)
        tree.heading('#0', text='')
        tree.heading('col2', text='Código Produto')
        tree.heading('col3', text='Nome Produto')
        tree.heading('col4', text='Quantidade')
        tree.heading('col5', text='Valor Unitário')
        tree.insert('', 'end', values=('123', 'Camiseta', '10', 'R$ 15,00'))
        tree.insert('', 'end', values=('456', 'Calcado', '5', 'R$ 50,00'))
        tree.grid(row=1, column=1)

    def entry_info(self):

        container = ctk.CTkFrame(self.root, bg_color="#2b2b2b",corner_radius=22)
        container.grid(row=1, column=0)

        nome_prod_label = ctk.CTkLabel(container, text="Informe o produto", bg_color="#2b2b2b")
        nome_prod_label.grid(row=0, column=0)
        nome_prod = ctk.CTkEntry(container,bg_color="#2b2b2b")
        nome_prod.grid(row=1, column=0)

        label_vazia = ctk.CTkLabel(container, text="vazioaaaaaaaaaa", bg_color="#2b2b2b", text_color="#2b2b2b")
        label_vazia.grid(row=1, column=2)

        venda_label = ctk.CTkLabel(container, text="Venda", bg_color="#2b2b2b")
        venda_label.grid(row=0, column=3, padx=10)
        venda = ctk.CTkEntry(container, bg_color="#2b2b2b")
        venda.grid(row=1, column=3)

        item_label = ctk.CTkLabel(container, text="Item", bg_color="#2b2b2b")
        item_label.grid(row=0, column=4, padx=10)
        item = ctk.CTkEntry(container, bg_color="#2b2b2b")
        item.grid(row=1, column=4)

        qtd_total_label = ctk.CTkLabel(container, text="Quantidade Total", bg_color="#2b2b2b")
        qtd_total_label.grid(row=0, column=5)
        qtd_total = ctk.CTkEntry(container, bg_color="#2b2b2b")
        qtd_total.grid(row=1, column=5)

        desc_label = ctk.CTkLabel(container, text="Descricão", bg_color="#2b2b2b")
        desc_label.grid(row=2, column=0)
        desc = ctk.CTkEntry(container, bg_color="#242424")
        desc.grid(row=3, column=0)

        complemento_label = ctk.CTkLabel(container, text="Complemento", bg_color="#2b2b2b")
        complemento_label.grid(row=4, column=0)
        complemento = ctk.CTkEntry(container, bg_color="#242424")
        complemento.grid(row=5, column=0)

        fator_label = ctk.CTkLabel(container, text="Fator", bg_color="#2b2b2b")
        fator_label.grid(row=6, column=0)
        fator = ctk.CTkEntry(container, bg_color="#2b2b2b")
        fator.grid(row=7, column=0)

        pecas_label = ctk.CTkLabel(container, text="Pecas", bg_color="#2b2b2b")
        pecas_label.grid(row=6, column=2)
        pecas = ctk.CTkEntry(container, bg_color="#2b2b2b")
        pecas.grid(row=7, column=2)

        qtd_label = ctk.CTkLabel(container, text="Quantidade", bg_color="#2b2b2b")
        qtd_label.grid(row=6, column=3)
        qtd = ctk.CTkEntry(container, bg_color="#2b2b2b")
        qtd.grid(row=7, column=3)

        unitario_label = ctk.CTkLabel(container, text="Unitário R$", bg_color="#2b2b2b")
        unitario_label.grid(row=6, column=4)
        unitario = ctk.CTkEntry(container, bg_color="#2b2b2b")
        unitario.grid(row=7, column=4)
        # receber o valor calculado
        total_label = ctk.CTkLabel(container, text="Total R$", bg_color="#2b2b2b")
        total_label.grid(row=6, column=5)
        total = ctk.CTkEntry(container, bg_color="#2b2b2b")
        total.grid(row=7, column=5)

        desconto_label = ctk.CTkLabel(container, text="Desconto", bg_color="#2b2b2b")
        desconto_label.grid(row=8, column=0)
        desconto = ctk.CTkEntry(container, bg_color="#2b2b2b")
        desconto.grid(row=9, column=0)

        acrescimo_label = ctk.CTkLabel(container, text="Acrescimo", bg_color="#2b2b2b")
        acrescimo_label.grid(row=10, column=0)
        acrescimo = ctk.CTkEntry(container, bg_color="#2b2b2b")
        acrescimo.grid(row=11, column=0)

        liquido_label = ctk.CTkLabel(container, text="Liquido R$", bg_color="#2b2b2b")
        liquido_label.grid(row=11, column=5)
        # receber o valor calculado
        liquido = ctk.CTkEntry(container, bg_color="#2b2b2b")
        liquido.grid(row=12, column=5)





if __name__ == "__main__":
    root = ctk.CTk()
    MainScreen(root)