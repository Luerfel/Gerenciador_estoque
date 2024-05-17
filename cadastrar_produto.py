import tkinter as tk
import fc
from tkinter import messagebox
import random
import oracledb
import customtkinter as ctk
from calculo_venda import CalculadoraPrecoVenda

# Conexão com o banco de dados Oracle
connection = oracledb.connect(user="SYSTEM", password="senha", host="localhost", port=1521)
cursor = connection.cursor()

class CadastrarProduto:
    def __init__(self, root):
        # Configurações iniciais da janela principal
        self.root = root
        self.root.title("Cadastro de Produtos")
        self.root.geometry("450x270")
        self.root.resizable(False, False)
        self.root.maxheight = 150
        
        # Chama a função para desenhar a interface de cadastro
        self.cadastro_design()
        
        # Inicia o loop principal da interface gráfica
        self.root.mainloop()

    def acessar_calculadora_preco_venda(self):
        # Função para acessar a calculadora de preço de venda
        self.root.withdraw()  # Oculta a janela principal
        calculadora = CalculadoraPrecoVenda(self.root)

    def voltar_tela_principal(self):
        # Função para voltar à tela principal
        self.root.iconify()  # Minimiza a janela principal
        self.nova_janela.destroy()  # Destroi a janela secundária

    def gerar_codigo_barra(self):
        # Função para gerar um código de barras único
        try:
            # Gera um código de barras de 13 dígitos
            self.codigo = "".join(str(random.randint(0, 9)) for _ in range(13))
            sql = "SELECT COUNT(*) FROM tbl_produtos WHERE codigo_de_barra = :codigo_de_barra"
            cursor.execute(sql, {"CODIGO_DE_BARRAS": self.codigo})
            resultado = cursor.fetchone()[0]
            if resultado > 0:
                return self.gerar_codigo_barra()  # Gera novamente se o código já existir
        except:
            fc.limpar_tela()
        return self.codigo

    def cadastro_design(self):
        # Desenha a interface de cadastro
        frame = ctk.CTkFrame(self.root)
        frame.place(relwidth=1, relheight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=3)

        # Nome do produto
        label_nome = ctk.CTkLabel(frame, text="Nome:")
        label_nome.grid(row=0, column=0, sticky=tk.W, pady=7, padx=15)
        self.entry_nome = ctk.CTkEntry(frame)
        self.entry_nome.grid(row=0, column=1, sticky=tk.EW, pady=7, padx=15)

        # Descrição do produto
        label_descricao = ctk.CTkLabel(frame, text="Descrição:")
        label_descricao.grid(row=1, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_descricao = ctk.CTkEntry(frame)
        self.entry_descricao.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=15)

        # Custo de aquisição do produto
        label_custo_aquisicao = ctk.CTkLabel(frame, text="Custo de Aquisição:")
        label_custo_aquisicao.grid(row=2, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_custo_aquisicao = ctk.CTkEntry(frame)
        self.entry_custo_aquisicao.grid(row=2, sticky=tk.EW, column=1, pady=5, padx=15)

        # Número de unidades do produto
        label_unidades = ctk.CTkLabel(frame, text="Unidades:")
        label_unidades.grid(row=3, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_unidades = ctk.CTkEntry(frame)
        self.entry_unidades.grid(row=3, column=1, sticky=tk.EW, pady=5, padx=15)

        # Fornecedor do produto
        label_fornecedor = ctk.CTkLabel(frame, text="Fornecedor:")
        label_fornecedor.grid(row=4, column=0, sticky=tk.W, pady=5, padx=15)
        self.combo_fornecedor = ctk.CTkComboBox(frame, state="readonly", values=["Fornecedor 1", "Fornecedor 2", "Fornecedor 3"])
        self.combo_fornecedor.grid(row=4, column=1, sticky=tk.EW, pady=5, padx=15)

        # Preço de venda do produto
        label_preco_venda_principal = ctk.CTkLabel(frame, text="Preço de Venda:")
        label_preco_venda_principal.grid(row=5, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_preco_venda_principal = ctk.CTkEntry(frame)
        self.entry_preco_venda_principal.grid(row=5, column=1, sticky=tk.EW, pady=5, padx=15)

        # Botão para calcular o preço de venda ao lado do campo de entrada
        botao_calcular_preco = ctk.CTkButton(frame, text="Calcular Preço de Venda", command=self.acessar_calculadora_preco_venda)
        botao_calcular_preco.grid(row=5, column=2, padx=5, pady=5)

        # Frame para botões de ação
        buttons_frame = ctk.CTkFrame(frame, fg_color="#2b2b2b")
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        buttons_frame.grid(row=6, column=0, columnspan=3, pady=4)

        # Botão para cadastrar o produto
        button_cadastrar = ctk.CTkButton(buttons_frame, text="Cadastrar Produto", command=self.cadastrar_produto)
        button_cadastrar.grid(row=0, column=0, padx=5, sticky=tk.W)

    def cadastrar_produto(self):
        # Função para cadastrar o produto no banco de dados
        self.nome = self.entry_nome.get()  # Obtém o nome do produto
        self.descricao = self.entry_descricao.get()  # Obtém a descrição do produto
        self.codigo_de_barras = self.gerar_codigo_barra()  # Gera um código de barras único
        self.preco_de_compra = self.entry_custo_aquisicao.get()  # Obtém o custo de aquisição
        self.preco_de_venda = self.entry_preco_venda_principal.get()  # Obtém o preço de venda
        self.unidades = self.entry_unidades.get()  # Obtém o número de unidades
        self.fornecedor = self.combo_fornecedor.get()  # Obtém o fornecedor

        # Validações dos campos
        if not fc.validar_nvarchar2(self.nome, 50, 1):
            return
        if not fc.validar_nvarchar2(self.descricao, 50, 0):
            return
        if not fc.validar_number("preço de venda", self.preco_de_venda, 1):
            return
        if not fc.validar_number("preço de compra", self.preco_de_compra, 1):
            return
        if not fc.validar_number("unidades", self.unidades, 1):
            return

        # Converte valores para tipos apropriados
        preco_de_venda = self.preco_de_venda.replace(',', '.')
        preco_de_venda = float(preco_de_venda)

        preco_de_compra = self.preco_de_compra.replace(',', '.')
        preco_de_compra = float(preco_de_compra)

        unidades = self.unidades.replace(',', '.')
        unidades = int(unidades)

        # Tenta inserir o produto no banco de dados
        try:
            cursor.execute("""
            INSERT INTO tbl_produtos (nome, descricao, codigo_de_barras, preco_de_compra, preco_de_venda, unidades, fornecedor)
            VALUES (:nome, :descricao, :codigo_de_barras, :preco_de_compra, :preco_de_venda, :unidades, :fornecedor)
            """, {
                'nome': self.nome,
                'descricao': self.descricao,
                'codigo_de_barras': self.codigo_de_barras,
                'preco_de_compra': preco_de_compra,
                'preco_de_venda': preco_de_venda,
                'unidades': unidades,
                'fornecedor': self.fornecedor
            })

            connection.commit()  # Confirma a transação

        except oracledb.DatabaseError as e:
            return

        # Limpa os campos de entrada após o cadastro
        self.entry_nome.delete(0, tk.END)
        self.entry_descricao.delete(0, tk.END)
        self.entry_custo_aquisicao.delete(0, tk.END)
        self.entry_preco_venda_principal.delete(0, tk.END)
        self.entry_unidades.delete(0, tk.END)
        self.combo_fornecedor.set("")

        # Exibe mensagem de sucesso
        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")

if __name__ == "__main__":
    root = ctk.CTk()  # Cria a janela principal
    CadastrarProduto(root)  # Inicia o cadastro de produto
