import tkinter as tk
import fc
from tkinter import ttk
from tkinter import messagebox
from tkinter import StringVar
import random
import oracledb
import customtkinter as ctk

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

# Caso seja a primeira vez Por favor Gere a tabela com o GerarTabela.py

connection = oracledb.connect(user="SYSTEM", password="senha", host="localhost", port=1521)
cursor = connection.cursor()


class CadastrarProduto():

    def __init__(self,root_parameter):
        self.root = root_parameter
        self.root.title("Cadastro de Produtos")
        self.root.geometry("450x270")
        self.root.resizable(False, False)
        self.root.maxheight = 150
        self.cadastro_design()
        self.root.mainloop()



    def salvar_preco_venda(self, preco_venda, label_preco_venda_principal):
        self.entry_preco_venda_principal.delete(0, tk.END)  # Limpa o conteúdo atual do Entry
        self.entry_preco_venda_principal.insert(0, preco_venda)  # Insere o preço de venda no Entry

        messagebox.showinfo("Sucesso", "Preço de venda calculado com sucesso!")


    def tela_calculo_venda(self):
        # Crie uma nova janela
        self.root.iconify()
        self.nova_janela = ctk.CTkToplevel(self.root)
        self.nova_janela.title("Calculadora de Preço de Venda")
        self.nova_janela.resizable(False, False)
        self.nova_janela.protocol("WM_DELETE_WINDOW", self.fechar_janela_calculo)

        # Adicione conteúdo à nova janela ctk
        frame = ctk.CTkFrame(self.nova_janela)
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.descricao(frame)

        # Campos de entrada custo fixo
        label_rendimento_mensal = ctk.CTkLabel(frame, text="Rendimento bruto Mensal:")
        label_rendimento_mensal.grid(row=0, column=0, sticky=tk.W, pady=2, padx=2)
        self.entry_rendimento_mensal = ctk.CTkEntry(frame, width=100)
        self.entry_rendimento_mensal.grid(row=0, column=1, sticky=tk.W, pady=2, padx=2)

        label_custo_fixo = ctk.CTkLabel(frame, text="Custo Fixo:")
        label_custo_fixo.grid(row=1, column=0, sticky=tk.W, pady=2, padx=2)
        self.entry_custo_fixo = ctk.CTkEntry(frame, width=100)
        self.entry_custo_fixo.grid(row=1, column=1, sticky=tk.W, pady=2, padx=2)

        label_custo_mercadoria = ctk.CTkLabel(frame, text="Custo total das Mercadorias:")
        label_custo_mercadoria.grid(row=0, column=4, sticky=tk.W, pady=2, padx=2)
        self.entry_custo_mercadoria = ctk.CTkEntry(frame, width=100)
        self.entry_custo_mercadoria.grid(row=0, column=5, sticky=tk.W, pady=2, padx=2)

        label_custo_operacional = ctk.CTkLabel(frame, text="Custo operacional:")
        label_custo_operacional.grid(row=1, column=4, sticky=tk.W, pady=2, padx=2)
        self.entry_custo_operacional = ctk.CTkEntry(frame, width=100)
        self.entry_custo_operacional.grid(row=1, column=5, sticky=tk.W, pady=2, padx=2)

        label_percentual_custo_fixo = ctk.CTkLabel(frame, text="Percentual do Custo Fixo:")
        label_percentual_custo_fixo.grid(row=5, column=0, sticky=tk.W, pady=1, padx=2)
        self.entry_percentual_custo_fixo = ctk.CTkEntry(frame, width=100, state="readonly")
        self.entry_percentual_custo_fixo.grid(row=5, column=1, sticky=tk.W, pady=1, padx=2)

        label_percentual_custo_operacional = ctk.CTkLabel(frame, text="Percentual do Custo Operacional:")
        label_percentual_custo_operacional.grid(row=6, column=0, sticky=tk.W, pady=1, padx=2)
        self.entry_percentual_custo_operacional = ctk.CTkEntry(frame, width=100, state="readonly")
        self.entry_percentual_custo_operacional.grid(row=6, column=1, sticky=tk.W, pady=1, padx=2)

        # Botão para calcular os percentuais
        btn_calcular = ctk.CTkButton(frame, text="Calcular Percentuais",
                                  command=lambda:    fc.calcular_custos_e_percentuais(self.entry_rendimento_mensal, self.entry_custo_fixo, self.entry_custo_mercadoria, 
                              self.entry_custo_operacional, self.entry_percentual_custo_fixo, self.entry_percentual_custo_operacional))
        btn_calcular.grid(row=3, columnspan=4, pady=10)

        # impostos
        label_custo_imposto = ctk.CTkLabel(frame, text="Percentual do imposto:")
        label_custo_imposto.grid(row=7, column=0, sticky=tk.W,pady=1, padx=2)
        self.entry_custo_imposto = ctk.CTkEntry(frame, width=100)
        self.entry_custo_imposto.grid(row=7, column=1, sticky=tk.W,pady=1, padx=2)

        # custo do produto
        label_custo_produto = ctk.CTkLabel(frame, text="Custo do Produto:")
        label_custo_produto.grid(row=8, column=0, sticky=tk.W,pady=1, padx=2)
        self.entry_custo_produto = ctk.CTkEntry(frame, width=100)
        self.entry_custo_produto.grid(row=8, column=1, sticky=tk.W,pady=1, padx=2)

        # comissão de venda
        label_comissao_venda = ctk.CTkLabel(frame, text="Percentual da Comissão Venda:")
        label_comissao_venda.grid(row=9, column=0, sticky=tk.W,pady=2, padx=2)
        self.entry_comissao_venda = ctk.CTkEntry(frame, width=100)
        self.entry_comissao_venda.grid(row=9, column=1, sticky=tk.W,pady=3, padx=2)

        # Margem de lucro
        label_margem_lucro = ctk.CTkLabel(frame, text="Percentual da Margem de Lucro:")
        label_margem_lucro.grid(row=10, column=0, sticky=tk.W,pady=3, padx=2)
        margem_lucro = StringVar()
        global margem_lucro_status_text
        margem_lucro_status_text = StringVar()
        margem_lucro_status_text.set("...")
        margem_lucro.trace("w", lambda name, index, mode, sv=margem_lucro: self.mostrar_lucro(sv))
        global label_margem_lucro_status
        label_margem_lucro_status = ctk.CTkLabel(frame, textvariable=margem_lucro_status_text)
        label_margem_lucro_status.grid(row=10, column=2, sticky=tk.W,pady=3, padx=2)
        self.entry_margem_lucro = ctk.CTkEntry(frame, width=100, textvariable=margem_lucro)
        self.entry_margem_lucro.grid(row=10, column=1, sticky=tk.W,pady=3, padx=2)

        label_preco_venda = ctk.CTkLabel(frame, text="Preço de Venda:")
        label_preco_venda.grid(row=11, column=0, sticky=tk.W,pady=3, padx=2)
        self.entry_preco_venda = ctk.CTkEntry(frame, width=100, state="readonly")
        self.entry_preco_venda.grid(row=11, column=1, sticky=tk.W,pady=3, padx=2)
        btn_calcular = ctk.CTkButton(frame, text="Calcular preço de venda",
                                  command=lambda: fc.calcular_preco_venda(self.entry_preco_venda_principal,self.entry_preco_venda,self.entry_custo_imposto,self.entry_margem_lucro,self.entry_comissao_venda,self.entry_custo_produto,self.entry_percentual_custo_fixo,self.entry_percentual_custo_operacional))
        btn_calcular.grid(row=12, columnspan=4, pady=10)
   
        # Botão "ctk"CTk
        btn_salvar = ctk.CTkButton(frame, text="Salvar",
                                command=lambda: self.salvar_preco_venda(self.entry_preco_venda.get(), self.entry_preco_venda_principal) or self.nova_janela.destroy())
        btn_salvar.grid(row=15, columnspan=4, pady=10)


        self.entry_preco_venda.get()

    def descricao(self, frame):
        # Configuração do frame de descrição dos itens
        self.descricao_frame = ctk.CTkFrame(frame)
        self.descricao_frame.grid(row=5, column=5, columnspan=2, rowspan=4)
        self.descricao_frame.grid_columnconfigure(0, weight=1)
        self.descricao_frame.grid_columnconfigure(1, weight=1)
        self.descricao_frame.grid_columnconfigure(2, weight=1)

        # Labels para os cabeçalhos das descrições
        label_header_descricao = ctk.CTkLabel(self.descricao_frame, text="Descricão")
        label_header_descricao.grid(row=0, column=0)

        label_desc_preco_venda = ctk.CTkLabel(self.descricao_frame, text="A.Preço de Venda")
        label_desc_preco_venda.grid(row=1, column=0)

        label_desc_custo_aquisicao = ctk.CTkLabel(self.descricao_frame, text="B.Custo de Aquisição")
        label_desc_custo_aquisicao.grid(row=2, column=0)

        label_desc_receita_bruta = ctk.CTkLabel(self.descricao_frame, text="C.Receita Bruta(A-B)")
        label_desc_receita_bruta.grid(row=3, column=0)

        label_desc_custo_fixo = ctk.CTkLabel(self.descricao_frame, text="D.Custo Fixo")
        label_desc_custo_fixo.grid(row=4, column=0)

        label_desc_impostos = ctk.CTkLabel(self.descricao_frame, text="E.Impostos")
        label_desc_impostos.grid(row=5, column=0)

        # Subframe para valores e percentuais
        self.descricao_subframe = ctk.CTkFrame(self.descricao_frame)
        self.descricao_subframe.grid(row=0, rowspan=6, column=2, sticky="ew")
        self.descricao_subframe.grid_columnconfigure(0, weight=1)
        self.descricao_subframe.grid_columnconfigure(1, weight=1)

        # Labels para valores
        label_header_valor = ctk.CTkLabel(self.descricao_subframe, text="Valor")
        label_header_valor.grid(row=0, column=0, padx=16, pady=3)

        label_val_preco_venda = ctk.CTkLabel(self.descricao_subframe, text="XX")
        label_val_preco_venda.grid(row=1, column=0, padx=16, pady=3)

        label_val_custo_aquisicao = ctk.CTkLabel(self.descricao_subframe, text="XX")
        label_val_custo_aquisicao.grid(row=2, column=0, padx=16, pady=3)

        label_val_receita_bruta = ctk.CTkLabel(self.descricao_subframe, text="XX")
        label_val_receita_bruta.grid(row=3, column=0, padx=16, pady=3)

        label_val_custo_fixo = ctk.CTkLabel(self.descricao_subframe, text="XX")
        label_val_custo_fixo.grid(row=4, column=0, padx=16, pady=3)

        label_val_impostos = ctk.CTkLabel(self.descricao_subframe, text="XX")
        label_val_impostos.grid(row=5, column=0, padx=16, pady=3)

        # Labels para percentuais
        label_header_percentual = ctk.CTkLabel(self.descricao_subframe, text="%")
        label_header_percentual.grid(row=0, column=1, padx=16, pady=3)

        label_perc_preco_venda = ctk.CTkLabel(self.descricao_subframe, text="X%")
        label_perc_preco_venda.grid(row=1, column=1, padx=16, pady=3)

        label_perc_custo_aquisicao = ctk.CTkLabel(self.descricao_subframe, text="X%")
        label_perc_custo_aquisicao.grid(row=2, column=1, padx=16, pady=3)

        label_perc_receita_bruta = ctk.CTkLabel(self.descricao_subframe, text="X%")
        label_perc_receita_bruta.grid(row=3, column=1, padx=16, pady=3)

        label_perc_custo_fixo = ctk.CTkLabel(self.descricao_subframe, text="X%")
        label_perc_custo_fixo.grid(row=4, column=1, padx=16, pady=3)

        label_perc_impostos = ctk.CTkLabel(self.descricao_subframe, text="X%")
        label_perc_impostos.grid(row=5, column=1, padx=16, pady=3)

    def voltar_tela_principal(self):
        # Retorna à tela principal ao fechar a janela atual
        self.root.iconify()
        self.nova_janela.destroy()

    def fechar_janela_calculo(self):
        # Fecha a janela de cálculo e retorna à tela principal
        self.root.deiconify()
        self.nova_janela.destroy()

    def gerar_codigo_barra(self):
        """
        Gera um código de barra único com 13 dígitos.

        Retorna:
        str: Código de barra.
        """

        try:
            # Gera string com 13 números aleatórios
            self.codigo = "".join(str(random.randint(0, 9)) for _ in range(13))

            # Verifica se o código já existe
            sql = """
            SELECT COUNT(*) FROM tbl_produtos WHERE codigo_de_barra = :codigo_de_barra
            """
            cursor.execute(sql, {"CODIGO_DE_BARRAS": self.codigo})
            resultado = cursor.fetchone()[0]
            # se o resultado for maior que 1 então significa que existe
            if resultado > 0:
                return self.gerar_codigo_barra()
        except:

            fc.limpar_tela()

        return self.codigo

    def cadastro_design(self):
        # Configura o design da interface de cadastro de produtos
        frame = ctk.CTkFrame(self.root)
        frame.place(relwidth=1, relheight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=3)

        # Campos de entrada para dados do produto
        label_nome = ctk.CTkLabel(frame, text="Nome:")
        label_nome.grid(row=0, column=0, sticky=tk.W, pady=7, padx=15)
        self.entry_nome = ctk.CTkEntry(frame)
        self.entry_nome.grid(row=0, column=1, sticky=tk.EW, pady=7, padx=15)

        label_descricao = ctk.CTkLabel(frame, text="Descrição:")
        label_descricao.grid(row=1, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_descricao = ctk.CTkEntry(frame)
        self.entry_descricao.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=15)

        label_custo_aquisicao = ctk.CTkLabel(frame, text="Custo de Aquisição:")
        label_custo_aquisicao.grid(row=2, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_custo_aquisicao = ctk.CTkEntry(frame)
        self.entry_custo_aquisicao.grid(row=2, sticky=tk.EW, column=1, pady=5, padx=15)

        label_unidades = ctk.CTkLabel(frame, text="Unidades:")
        label_unidades.grid(row=3, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_unidades = ctk.CTkEntry(frame)
        self.entry_unidades.grid(row=3, column=1, sticky=tk.EW, pady=5, padx=15)

        label_fornecedor = ctk.CTkLabel(frame, text="Fornecedor:")
        label_fornecedor.grid(row=4, column=0, sticky=tk.W, pady=5, padx=15)
        self.combo_fornecedor = ctk.CTkComboBox(frame, state="readonly", values=["Fornecedor 1", "Fornecedor 2", "Fornecedor 3"])  # Aqui você pode adicionar os fornecedores cadastrados
        self.combo_fornecedor.grid(row=4, column=1, sticky=tk.EW, pady=5, padx=15)

        label_preco_venda_principal = ctk.CTkLabel(frame, text="Preço de Venda:")
        label_preco_venda_principal.grid(row=5, column=0, sticky=tk.W, pady=5, padx=15)
        self.entry_preco_venda_principal = ctk.CTkEntry(frame)
        self.entry_preco_venda_principal.grid(row=5, sticky=tk.EW, column=1, pady=5, padx=15)

        # Frame para botões
        buttons_frame = ctk.CTkFrame(frame, fg_color="#2b2b2b")
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        buttons_frame.grid(row=6, column=0, columnspan=2, pady=4)

        # Botão para acessar a tela de cálculo de preço de venda
        botao_nova_tela = ctk.CTkButton(buttons_frame, text="Calcular Preço de venda", command=self.tela_calculo_venda)
        botao_nova_tela.grid(row=0, column=1, padx=5, sticky=tk.W)

        # Botão para cadastrar produto
        button_cadastrar = ctk.CTkButton(buttons_frame, text="Cadastrar Produto", command=self.cadastrar_produto)
        button_cadastrar.grid(row=0, column=0, padx=5, sticky=tk.W)

    def mostrar_lucro(self,margem_lucro):
        # Função que mostra se a margem de lucro esta boa

        # Verifica se o campo da margem de lucro está vazio
        if margem_lucro.get() == "":
            # Define o texto de status como indefinido e a cor como preta
            margem_lucro_status_text.set("...")
            label_margem_lucro_status.configure(text_color="white")

        # Verifica se a margem de lucro está entre 0 e 15 (Baixo)
        elif float(margem_lucro.get()) >= 0 and float(margem_lucro.get()) <= 15:
            margem_lucro_status_text.set("Baixo")
            label_margem_lucro_status.configure(text_color="red")

        # Verifica se a margem de lucro está entre 15 e 30 (Moderado)
        elif float(margem_lucro.get()) > 15 and float(margem_lucro.get()) <= 30:
            margem_lucro_status_text.set("Moderado")
            label_margem_lucro_status.configure(text_color="orange")

        # Verifica se a margem de lucro está entre 30 e 45 (Alto)
        elif float(margem_lucro.get()) > 30 and float(margem_lucro.get()) <= 45:
            margem_lucro_status_text.set("Alto")
            label_margem_lucro_status.configure(text_color="green")

        # Verifica se a margem de lucro é maior que 45 (Muito Alto)
        elif float(margem_lucro.get()) > 45:
            margem_lucro_status_text.set("Muito Alto")
            label_margem_lucro_status.configure(text_color="blue")

        # Se o valor inserido não for válido
        else:
            # Define o texto de status como "Insira um valor maior que 0" e a cor como preta
            margem_lucro_status_text.set("Insira um valor maior que 0")
            label_margem_lucro_status.configure(text_color="white")


    def cadastrar_produto(self):
        # Obter os valores dos campos
        self.nome = self.entry_nome.get()
        self.descricao = self.entry_descricao.get()
        self.codigo_de_barras = self.gerar_codigo_barra()
        self.preco_de_compra = self.entry_custo_aquisicao.get()
        self.preco_de_venda = self.entry_preco_venda_principal.get()
        self.unidades = self.entry_unidades.get()
        self.fornecedor = self.combo_fornecedor.get()

        # Validar os campos
        if not fc.validar_nvarchar2(self.nome, 50, 1):
            return
        if not fc.validar_nvarchar2(self.descricao, 50, 0):
            return
        if not fc.validar_number("preco de venda", self.preco_de_venda, 1):
            return
        if not fc.validar_number("preço de compra", self.preco_de_compra, 1):
            return
        if not fc.validar_number("unidades", self.unidades, 1):
            return

        # converte os valores
        preco_de_venda = self.preco_de_venda.replace(',', '.')  # substitui a virgula pelo ponto antes de converter para float
        preco_de_venda = float(preco_de_venda)

        preco_de_compra = self.preco_de_compra.replace(',', '.')
        preco_de_compra = float(preco_de_compra)

        unidades = self.unidades.replace(',', '.')
        unidades = int(unidades)

        # adiciona ao banco de dados
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

            connection.commit()  # Salva as alterações no banco de dados



        except oracledb.DatabaseError as e:
            return



        # Limpar campos após o cadastro
        self.entry_nome.delete(0, tk.END)
        self.entry_descricao.delete(0, tk.END)
        self.entry_custo_aquisicao.delete(0, tk.END)
        self.entry_preco_venda_principal.delete(0, tk.END)
        self.entry_unidades.delete(0, tk.END)
        self.combo_fornecedor.set("")  # Limpar a seleção do fornecedor

        # Mostrar mensagem de sucesso
        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")


if __name__ == "__main__":
    root = ctk.CTk()
    CadastrarProduto(root)
