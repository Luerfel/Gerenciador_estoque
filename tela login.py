import customtkinter as ctk
from tkinter import messagebox
from commons import Commons
from TelaMain import MainScreen
import sqlite3

class TelaLogin(Commons):

    def __init__(self, root_parameter):
        self.root = root_parameter
        self.montar_tela_login()
        self.login_design()
        self.root.mainloop()

    def montar_tela_login(self):
        self.root.geometry("300x300")
        self.root.title("Login")
        self.root.resizable(False, False)
        self.root.configure(background="#ffffff")

    def login_design(self):
        self.username_label = ctk.CTkLabel(self.root, text="Username:", bg_color="#242424")
        self.username_label.pack()
        self.username_entry = ctk.CTkEntry(self.root, width=130)
        self.username_entry.pack(pady=7)

        self.password_label = ctk.CTkLabel(self.root, text="Password:", bg_color="#242424")
        self.password_label.pack()
        self.password_entry = ctk.CTkEntry(self.root, width=130, show="*")
        self.password_entry.pack(pady=7)

        self.login_button = ctk.CTkButton(self.root, text="Login", bg_color="#3b43a9", hover_color="#5662f6",command=self.login_validation)
        self.login_button.pack(pady=10)

    def login_validation(self):
        real_password = ""

        username = self.username_entry.get()
        password = self.password_entry.get()

        self.username_entry.bind("<Return>", lambda event: self.login_validation())
        self.password_entry.bind("<Return>", lambda event: self.login_validation())

        if username == "" and password == "":
            messagebox.showinfo("Login", "Login efetuado com sucesso!")
            self.username_label.destroy()
            self.username_entry.destroy()
            self.password_label.destroy()
            self.password_entry.destroy()
            self.login_button.destroy()
            MainScreen(self.root)
        else:
            messagebox.showerror("Erro", "Login inválido. Verifique os dados e tente novamente.")
            self.username_entry.delete(0, ctk.END)
            self.password_entry.delete(0, ctk.END)

if __name__ == "__main__":
    root = ctk.CTk()
    TelaLogin(root)