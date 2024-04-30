import customtkinter as ctk  # Importa a biblioteca personalizada de tkinter com alias "ctk"
from tkinter import messagebox  # Importa a classe de messagebox do módulo tkinter
from commons import Commons  # Importa a classe Commons do módulo commons
from TelaMain import MainScreen  # Importa a classe MainScreen do módulo TelaMain

class TelaLogin(Commons):
    def __init__(self, root_parameter):
        """
        Inicializa a tela de login.

        Args:
        root_parameter (tk.Tk): O objeto da janela principal tkinter.
        """
        self.root = root_parameter  # Define a janela principal
        self.montar_tela_login()  # Chama o método para montar a tela de login
        self.login_design()  # Chama o método para configurar o design do login
        self.root.mainloop()  # Inicia o loop principal da interface gráfica

    def montar_tela_login(self):
        """Define as configurações iniciais da janela de login."""
        self.root.geometry("300x300")  # Define o tamanho da janela
        self.root.title("Login")  # Define o título da janela
        self.root.resizable(False, False)  # Impede o redimensionamento da janela
        self.root.configure(background="#ffffff")  # Define a cor de fundo da janela

    def login_design(self):
        """Configura o design da interface de login."""
        # Label e campo de entrada para o nome de usuário
        self.username_label = ctk.CTkLabel(self.root, text="Username:", bg_color="#242424")
        self.username_label.pack()
        self.username_entry = ctk.CTkEntry(self.root, width=130)
        self.username_entry.pack(pady=7)

        # Label e campo de entrada para a senha
        self.password_label = ctk.CTkLabel(self.root, text="Password:", bg_color="#242424")
        self.password_label.pack()
        self.password_entry = ctk.CTkEntry(self.root, width=130, show="*")
        self.password_entry.pack(pady=7)

        # Botão de login
        self.login_button = ctk.CTkButton(self.root, text="Login", bg_color="#3b43a9", hover_color="#5662f6", command=self.login_validation)
        self.login_button.pack(pady=10)

    def login_validation(self):
        """Valida as credenciais de login."""
        real_password = ""  # Define a senha real (aqui deve ser implementada a lógica para verificar a senha real)

        # Obtém o nome de usuário e a senha inseridos pelo usuário
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Configura o evento de pressionar "Enter" nos campos de entrada para chamar a validação de login
        self.username_entry.bind("<Return>", lambda event: self.login_validation())
        self.password_entry.bind("<Return>", lambda event: self.login_validation())

        # Verifica se os campos de entrada estão vazios
        if username == "" and password == "":
            messagebox.showinfo("Login", "Login efetuado com sucesso!")  # Exibe uma mensagem de sucesso
            # Destroi os elementos da interface de login e chama a tela principal
            self.username_label.destroy()
            self.username_entry.destroy()
            self.password_label.destroy()
            self.password_entry.destroy()
            self.login_button.destroy()
            MainScreen(self.root)  # Chama a tela principal após o login bem-sucedido
        else:
            messagebox.showerror("Erro", "Login inválido. Verifique os dados e tente novamente.")  # Exibe uma mensagem de erro
            self.username_entry.delete(0, ctk.END)  # Limpa o campo de entrada do nome de usuário
            self.password_entry.delete(0, ctk.END)  # Limpa o campo de entrada da senha

if __name__ == "__main__":
    root = ctk.CTk()  # Cria uma nova instância da janela principal tkinter
    TelaLogin(root)  # Inicializa a tela de login com a janela principal
