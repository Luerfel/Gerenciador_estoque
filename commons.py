from tkinter import messagebox
from CadastrarProduto import CadastrarProduto
import tkinter as tk

class Commons():
    def confirm_exit(self):
        if messagebox.askyesno("Saída", "Você tem certeza que deseja sair?"):
            self.root.destroy()


    def design(self):
        """função comum para fazer o design da
        toolbar"""
        self.menu_bar = tk.Menu(self.root, tearoff=0)
        self.cadastro_file = tk.Menu(self.menu_bar, tearoff=0)
        self.cadastro_file.add_command(label="1-Cadastrar",command=self.cadastrar)
        self.cadastro_file.add_command(label="2-Listar")
        self.menu_bar.add_cascade(label="1-Cadastrar", menu=self.cadastro_file)
        self.editar_file = tk.Menu(self.menu_bar, tearoff=0)
        self.editar_file.add_command(label="1-Editar produtos")
        self.editar_file.add_command(label="2-Editar fornecedores")
        self.menu_bar.add_cascade(label="2-Editar", menu=self.editar_file)
        self.menu_bar.add_command(label="3-Excluir")
        self.menu_bar.add_command(label="4-Configuração")
        self.menu_bar.add_command(label="5-Sair", command=self.confirm_exit)

        self.root.config(menu=self.menu_bar)

    def cadastrar(self):
        self.root.wm_state('iconic')
        root = tk.Tk()
        CadastrarProduto(root)
