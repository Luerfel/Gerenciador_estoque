# Importação das bibliotecas necessárias
import tkinter as tk  # Biblioteca padrão do Tkinter para a criação de interfaces gráficas
import customtkinter as ctk  # Biblioteca customizada para estilização do Tkinter
from tkinter import ttk, messagebox  # Importa componentes adicionais do Tkinter
import oracledb  # Biblioteca para conectar-se ao banco de dados Oracle

# **Observações:**
# Este código utiliza um banco de dados local para armazenar as informações.
# Altere as variáveis `user`, `password`, `host`, `port` para conectar-se ao seu banco de dados.

# **Detalhes da conexão:**
# * **user:** Nome de usuário do banco de dados.
# * **password:** Senha do banco de dados.
# * **host:** Nome do serviço do banco de dados.
# * **port:** Porta do serviço do banco de dados.

# Estabelece a conexão com o banco de dados Oracle.
connection = oracledb.connect(user="SYSTEM", password="senha", host="localhost", port=1521)
cursor = connection.cursor()  

# Classe para a janela de consulta de produtos
class ConsultarProduto():
    def __init__(self, root_parameter):
        self.root = root_parameter  # Janela principal da aplicação
        self.root.title("Consultar Produto")  # Define o título da janela
        self.consultar_design()  # Chama o método para desenhar a interface
        self.carregar_produtos()  # Carrega os produtos existentes no banco de dados
        self.root.mainloop()  # Inicia o loop principal da interface gráfica

    # Método para carregar os produtos do banco de dados na árvore de visualização
    def carregar_produtos(self):
        sql = "SELECT codigo_de_barras, nome, descricao, preco_de_compra, preco_de_venda, fornecedor FROM tbl_produtos"
        cursor.execute(sql)  # Executa o comando SQL
        produtos = cursor.fetchall()  # Busca todos os resultados da consulta
        for produto in produtos:  # Itera sobre os produtos retornados
            codigo, nome, descricao, preco_de_compra, preco_de_venda, fornecedor = produto  # Desempacota os valores do produto
            self.tree.insert("", "end", values=(codigo, nome, descricao, preco_de_compra, preco_de_venda, fornecedor))  # Insere os produtos na árvore

    # Método para buscar um produto específico no banco de dados
    def buscar_produto(self):
        termo_busca = self.entry_busca.get()  # Obtém o termo de busca inserido pelo usuário
        tipo_busca = self.combo_tipo_busca.get()  # Obtém o tipo de busca selecionado pelo usuário
        if tipo_busca == "Código de Barras":  # Verifica se a busca é por código de barras
            sql = "SELECT codigo_de_barras, nome, descricao, preco_de_compra, preco_de_venda, fornecedor FROM tbl_produtos WHERE codigo_de_barras = :TERMOS_BUSCA"
        else:  # Caso contrário, a busca será por nome
            sql = "SELECT codigo_de_barras, nome, descricao, preco_de_compra, preco_de_venda, fornecedor FROM tbl_produtos WHERE nome LIKE :TERMOS_BUSCA"
        cursor.execute(sql, {"TERMOS_BUSCA": termo_busca})  # Executa o comando SQL com o termo de busca
        resultados = cursor.fetchall()  
        if resultados:  #
            self.tree.delete(*self.tree.get_children())  # 
            for produto in resultados:  
                codigo, nome, descricao, preco_de_compra, preco_de_venda, fornecedor = produto  
                self.tree.insert("", "end", values=(codigo, nome, descricao, preco_de_compra, preco_de_venda, fornecedor))  
        else:
            messagebox.showerror("Erro", "Nenhum resultado encontrado.")  

    # Método para desenhar a interface de consulta de produtos
    def consultar_design(self):
        frame = ctk.CTkFrame(self.root)  # Cria um frame principal
        frame.pack(fill=ctk.BOTH, expand=True)  # Adiciona o frame à janela principal

        label_titulo = ctk.CTkLabel(frame, text="Consulta de Produtos")  # Cria um rótulo com o título
        label_titulo.pack()  # Adiciona o rótulo ao frame

        frame_busca = ctk.CTkFrame(frame)  # Cria um frame para a área de busca
        frame_busca.pack(fill=tk.X)  #

        label_busca = ctk.CTkLabel(frame_busca, text="Buscar Produto:")  # Cria um rótulo para o campo de busca
        label_busca.pack(side=tk.LEFT)  # Adiciona o rótulo ao frame de busca

        self.entry_busca = ctk.CTkEntry(frame_busca)  # Cria um campo de entrada de texto para a busca
        self.entry_busca.pack(side=ctk.LEFT, padx=5, fill=ctk.X, expand=True)  # Adiciona o campo de entrada ao frame de busca

        self.combo_tipo_busca = ttk.Combobox(frame_busca, values=["Código de Barras", "Nome"], state="readonly")  # Cria um combobox para selecionar o tipo de busca
        self.combo_tipo_busca.pack(side=ctk.LEFT)  # Adiciona o combobox ao frame de busca
        self.combo_tipo_busca.current(0)  # Define o valor padrão como "Código de Barras"

        button_buscar = ctk.CTkButton(frame_busca, text="Buscar", command=self.buscar_produto)  # Cria um botão para iniciar a busca
        button_buscar.pack(side=ctk.LEFT)  

        self.tree = ttk.Treeview(frame, columns=("Código de Barras", "Nome", "Descrição", "Preço Compra", "Preço Venda", "Fornecedor"), show="headings")  # Cria uma árvore de visualização para os produtos
        self.tree.heading("Código de Barras", text="Código de Barras")  
        self.tree.heading("Nome", text="Nome") 
        self.tree.heading("Descrição", text="Descrição")  
        self.tree.heading("Preço Compra", text="Preço Compra")  
        self.tree.heading("Preço Venda", text="Preço Venda")  
        self.tree.heading("Fornecedor", text="Fornecedor")  
        self.tree.pack(fill=ctk.BOTH, expand=True)  # Adiciona a árvore ao frame principal

# Executa a aplicação
if __name__ == "__main__":
    root = ctk.CTk()  # Cria a janela principal
    ConsultarProduto(root)  # Instancia a classe ConsultarProduto e inicia a aplicação
