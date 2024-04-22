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

connection = oracledb.connect(user="SYSTEM", password="senha", host="localhost", port=1521)
cursor = connection.cursor()

class EditarProduto():
    def __init__(self, root_parameter):
        self.root = root_parameter
        self.root.title("Editar Produto")
        self.editar_design()
        self.root.mainloop()

    def tela_calculo_venda(self):
        # Crie uma nova janela
        self.root.iconify()
        self.nova_janela = tk.Toplevel(self.root)
        self.nova_janela.title("Calculadora de Preço de Venda")
        self.nova_janela.protocol("WM_DELETE_WINDOW", self.fechar_janela_calculo)