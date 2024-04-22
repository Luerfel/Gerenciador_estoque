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

# Caso seja a primeira vez Por favor Gere a tabela com o GerarTabela.py

connection = oracledb.connect(user="SYSTEM", password="testador", host="localhost", port="1521")
cursor = connection.cursor()


class CadastrarProduto():

    def __init__(self,root_parameter):
        self.root = root_parameter
        self.root.title("Cadastro de Produtos")
        self.cadastro_design()
        self.root.mainloop()

    def calcular_preco_venda(self,ca, entry_iv, entry_cf, entry_co, entry_ml, entry_cv, entry_preco_venda):
        self.ca = float(ca.get())
        print(self.ca, " Custo do produto")
        self.iv = float(entry_iv.get())
        print(self.iv, " Imposto")
        self.cf = float(entry_cf.get())
        print(self.cf, "custo fixo")
        self.co = float(entry_co.get())
        print(self.co, "custo operacionail")
        self.ml = float(entry_ml.get())
        print(self.ml, " Margem lucro")
        self.cv = float(entry_cv.get())
        print(self.cv, "preço venda")
        self.preco_venda = self.ca / (1 - (self.iv + self.cf + self.co + self.ml + self.cv) / 100)
        try:
            entry_preco_venda.config(state="normal")
            entry_preco_venda.delete(0, tk.END)
            entry_preco_venda.insert(0, "{:.2f}".format(self.preco_venda))
            entry_preco_venda.config(state="readonly")
        except:
            entry_preco_venda.config(state="normal")
            entry_preco_venda.delete(0, tk.END)
            entry_preco_venda.insert(0, "Erro")
            entry_preco_venda.config(state="readonly")


    def calcular_percentuais(self,entry_rendimento_mensal, entry_custo_fixo, entry_custo_mercadoria, entry_custo_operacional,
                             entry_percentual_custo_fixo, entry_percentual_custo_operacional):
        # função auxiliar para o calcular_porcentagem_custo fazer o calculo 2x
        self.calcular_porcentagem_custo(entry_rendimento_mensal, entry_custo_fixo, entry_percentual_custo_fixo,
                                   "rendimento mensal")
        self.calcular_porcentagem_custo(entry_custo_mercadoria, entry_custo_operacional, entry_percentual_custo_operacional,
                                   "custo total das mercadorias")

    def calcular_porcentagem_custo(referencia, custo, entry_resultado, tipo):
        try:
            valor_referencia = float(referencia.get())
            valor_custo = float(custo.get())
            percentual_custo = (valor_custo / valor_referencia) * 100
            entry_resultado.config(state="normal")
            entry_resultado.delete(0, tk.END)
            entry_resultado.insert(0, "{:.2f}".format(percentual_custo))
            entry_resultado.config(state="readonly")

        except ValueError:
            # Se valores inseridos não forem números
            entry_resultado.config(state="normal")
            entry_resultado.delete(0, tk.END)
            entry_resultado.insert(0, "Erro")
            entry_resultado.config(state="readonly")


    def salvar_preco_venda(self, preco_venda, label_preco_venda_principal):
        self.entry_preco_venda_principal.delete(0, tk.END)  # Limpa o conteúdo atual do Entry
        self.entry_preco_venda_principal.insert(0, preco_venda)  # Insere o preço de venda no Entry

        messagebox.showinfo("Sucesso", "Preço de venda calculado com sucesso!")


    def tela_calculo_venda(self):
        # Crie uma nova janela
        self.root.iconify()
        self.nova_janela = tk.Toplevel(self.root)
        self.nova_janela.title("Calculadora de Preço de Venda")
        self.nova_janela.protocol("WM_DELETE_WINDOW", self.fechar_janela_calculo)

        # Adicione conteúdo à nova janela
        frame = ttk.Frame(self.nova_janela, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Campos de entrada custo fixo
        label_rendimento_mensal = ttk.Label(frame, text="Rendimento bruto Mensal:")
        label_rendimento_mensal.grid(row=0, column=0, sticky=tk.W)
        entry_rendimento_mensal = ttk.Entry(frame, width=15)
        entry_rendimento_mensal.grid(row=0, column=1, sticky=tk.W)

        label_custo_fixo = ttk.Label(frame, text="Custo Fixo:")
        label_custo_fixo.grid(row=1, column=0, sticky=tk.W)
        entry_custo_fixo = ttk.Entry(frame, width=15)
        entry_custo_fixo.grid(row=1, column=1, sticky=tk.W)

        label_custo_mercadoria = ttk.Label(frame, text="Custo total das Mercadorias:")
        label_custo_mercadoria.grid(row=0, column=4, sticky=tk.W)
        entry_custo_mercadoria = ttk.Entry(frame, width=15)
        entry_custo_mercadoria.grid(row=0, column=5, sticky=tk.W)

        label_custo_operacional = ttk.Label(frame, text="Custo operacional:")
        label_custo_operacional.grid(row=1, column=4, sticky=tk.W)
        entry_custo_operacional = ttk.Entry(frame, width=15)
        entry_custo_operacional.grid(row=1, column=5, sticky=tk.W)

        label_percentual_custo_fixo = ttk.Label(frame, text="Percentual do Custo Fixo:")
        label_percentual_custo_fixo.grid(row=5, column=0, sticky=tk.W)
        entry_percentual_custo_fixo = ttk.Entry(frame, width=15, state="readonly")
        entry_percentual_custo_fixo.grid(row=5, column=1, sticky=tk.W)

        label_percentual_custo_operacional = ttk.Label(frame, text="Percentual do Custo Operacional:")
        label_percentual_custo_operacional.grid(row=6, column=0, sticky=tk.W)
        entry_percentual_custo_operacional = ttk.Entry(frame, width=15, state="readonly")
        entry_percentual_custo_operacional.grid(row=6, column=1, sticky=tk.W)

        # Botão para calcular os percentuais
        btn_calcular = ttk.Button(frame, text="Calcular Percentuais",
                                  command=lambda: self.calcular_percentuais(entry_rendimento_mensal, entry_custo_fixo,
                                                                       entry_custo_mercadoria, entry_custo_operacional,
                                                                       entry_percentual_custo_fixo,
                                                                       entry_percentual_custo_operacional))
        btn_calcular.grid(row=3, columnspan=4, pady=10)

        # impostos
        label_custo_imposto = ttk.Label(frame, text="Percentual do imposto:")
        label_custo_imposto.grid(row=7, column=0, sticky=tk.W)
        entry_custo_imposto = ttk.Entry(frame, width=15)
        entry_custo_imposto.grid(row=7, column=1, sticky=tk.W)

        # impostos
        label_custo_produto = ttk.Label(frame, text="Custo do Produto:")
        label_custo_produto.grid(row=8, column=0, sticky=tk.W)
        entry_custo_produto = ttk.Entry(frame, width=15)
        entry_custo_produto.grid(row=8, column=1, sticky=tk.W)

        # comissão de venda
        label_comissao_venda = ttk.Label(frame, text="Percentual da Comissão Venda:")
        label_comissao_venda.grid(row=9, column=0, sticky=tk.W)
        entry_comissao_venda = ttk.Entry(frame, width=15)
        entry_comissao_venda.grid(row=9, column=1, sticky=tk.W)

        # Margem de lucro
        label_margem_lucro = ttk.Label(frame, text="Percentual da Margem de Lucro:")
        label_margem_lucro.grid(row=10, column=0, sticky=tk.W)
        margem_lucro = StringVar()
        global margem_lucro_status_text
        margem_lucro_status_text = StringVar()
        margem_lucro_status_text.set("...")
        margem_lucro.trace("w", lambda name, index, mode, sv=margem_lucro: self.mostrar_lucro(sv))
        global label_margem_lucro_status
        label_margem_lucro_status = ttk.Label(frame, textvariable=margem_lucro_status_text)
        label_margem_lucro_status.grid(row=10, column=2, sticky=tk.W)
        global entry_margem_lucro
        entry_margem_lucro = ttk.Entry(frame, width=15, textvariable=margem_lucro)
        entry_margem_lucro.grid(row=10, column=1, sticky=tk.W)

        label_preco_venda = ttk.Label(frame, text="Preço de Venda:")
        label_preco_venda.grid(row=11, column=0, sticky=tk.W)
        entry_preco_venda = ttk.Entry(frame, width=15, state="readonly")
        entry_preco_venda.grid(row=11, column=1, sticky=tk.W)
        btn_calcular = ttk.Button(frame, text="Calcular preço de venda",
                                  command=lambda: self.calcular_preco_venda(entry_custo_produto, entry_custo_imposto,
                                                                       entry_percentual_custo_fixo,
                                                                       entry_percentual_custo_operacional,
                                                                       entry_margem_lucro, entry_comissao_venda,
                                                                       entry_preco_venda))
        btn_calcular.grid(row=12, columnspan=4, pady=10)

        # Botão "Salvar"
        btn_salvar = ttk.Button(frame, text="Salvar",
                                command=lambda: self.salvar_preco_venda(entry_preco_venda.get(), self.label_preco_venda_principal))
        btn_salvar.grid(row=15, columnspan=4, pady=10)


        entry_preco_venda.get()

    def voltar_tela_principal(self):
        self.root.iconify()
        self.nova_janela.destroy()

    def fechar_janela_calculo(self):
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
            codigo = "".join(str(random.randint(0, 9)) for _ in range(13))

            # Verifica se o código já existe
            sql = """
            SELECT COUNT(*) FROM tbl_produtos WHERE codigo_de_barra = :codigo_de_barra
            """
            cursor.execute(sql, {"CODIGO_DE_BARRAS": codigo})
            resultado = cursor.fetchone()[0]
            # se o resultado for maior que 1 então significa que existe
            if resultado > 0:
                return self.gerar_codigo_barra()
        except:

            fc.limpar_tela()

        return self.codigo


    def mostrar_lucro(self,margem_lucro):
        # Função que mostra se a margem de lucro esta boa

        # Verifica se o campo da margem de lucro está vazio
        if margem_lucro.get() == "":
            # Define o texto de status como indefinido e a cor como preta
            margem_lucro_status_text.set("...")
            label_margem_lucro_status.configure(foreground="black")

        # Verifica se a margem de lucro está entre 0 e 15 (Baixo)
        elif float(margem_lucro.get()) >= 0 and float(margem_lucro.get()) <= 15:
            margem_lucro_status_text.set("Baixo")
            label_margem_lucro_status.configure(foreground="red")

        # Verifica se a margem de lucro está entre 15 e 30 (Moderado)
        elif float(margem_lucro.get()) > 15 and float(margem_lucro.get()) <= 30:
            margem_lucro_status_text.set("Moderado")
            label_margem_lucro_status.configure(foreground="orange")

        # Verifica se a margem de lucro está entre 30 e 45 (Alto)
        elif float(margem_lucro.get()) > 30 and float(margem_lucro.get()) <= 45:
            margem_lucro_status_text.set("Alto")
            label_margem_lucro_status.configure(foreground="green")

        # Verifica se a margem de lucro é maior que 45 (Muito Alto)
        elif float(margem_lucro.get()) > 45:
            margem_lucro_status_text.set("Muito Alto")
            label_margem_lucro_status.configure(foreground="blue")

        # Se o valor inserido não for válido
        else:
            # Define o texto de status como "Insira um valor maior que 0" e a cor como preta
            margem_lucro_status_text.set("Insira um valor maior que 0")
            label_margem_lucro_status.configure(foreground="black")


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


# Frame para agrupar os campos
    def cadastro_design(self):
        frame = ttk.Frame(self.root, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Campos de entrada
        label_nome = ttk.Label(frame, text="Nome:")
        label_nome.grid(row=0, column=0, sticky=tk.W)
        entry_nome = ttk.Entry(frame, width=50)
        entry_nome.grid(row=0, column=1, sticky=tk.W)

        label_descricao = ttk.Label(frame, text="Descrição:")
        label_descricao.grid(row=1, column=0, sticky=tk.W)
        entry_descricao = ttk.Entry(frame, width=50)
        entry_descricao.grid(row=1, column=1, sticky=tk.W)

        label_custo_aquisicao = ttk.Label(frame, text="Custo de Aquisição:")
        label_custo_aquisicao.grid(row=2, column=0, sticky=tk.W)
        entry_custo_aquisicao = ttk.Entry(frame, width=50)
        entry_custo_aquisicao.grid(row=2, column=1, sticky=tk.W)

        label_unidades = ttk.Label(frame, text="Unidades:")
        label_unidades.grid(row=3, column=0, sticky=tk.W)
        entry_unidades = ttk.Entry(frame, width=50)
        entry_unidades.grid(row=3, column=1, sticky=tk.W)

        label_fornecedor = ttk.Label(frame, text="Fornecedor:")
        label_fornecedor.grid(row=4, column=0, sticky=tk.W)
        combo_fornecedor = ttk.Combobox(frame, width=47, state="readonly")
        combo_fornecedor['values'] = ("Fornecedor 1", "Fornecedor 2", "Fornecedor 3")  # Aqui você pode adicionar os fornecedores cadastrados
        combo_fornecedor.grid(row=4, column=1, sticky=tk.W)

        label_preco_venda_principal = ttk.Label(frame, text="Preço de Venda:")
        label_preco_venda_principal.grid(row=5, column=0, sticky=tk.W)
        entry_preco_venda_principal = ttk.Entry(frame, width=50)
        entry_preco_venda_principal.grid(row=5, column=1, sticky=tk.W)

        botao_nova_tela = ttk.Button(frame, text="Calcular Preço de venda", command=self.tela_calculo_venda)
        botao_nova_tela.grid(row=5, column=2, padx=10, sticky=tk.W)

        # Botão para cadastrar produto
        button_cadastrar = ttk.Button(frame, text="Cadastrar Produto", command=self.cadastrar_produto)
        button_cadastrar.grid(row=6, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    CadastrarProduto(root)