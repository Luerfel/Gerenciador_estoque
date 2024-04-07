import tkinter as tk
import fc
from tkinter import ttk
from tkinter import messagebox
import random
import oracledb # biblioteca da oracle

# Estabelece a conexão com o banco de dados Oracle.

# **Observações:**

# * Este código utiliza um banco de dados local para armazenar as informações.
# * Altere as variáveis `user`, `password`, `dsn` e `sid` para conectar-se ao seu banco de dados.

# **Detalhes da conexão:**

# * **user:** Nome de usuário do banco de dados.
# * **password:** Senha do banco de dados.
# * **host:** Nome do serviço do banco de dados.
# * **sid:** SID (System Identifier) do banco de dados.


connection = oracledb.connect (user="SYSTEM",password="senha",host="localhost",port=1521)
cursor = connection.cursor()


import tkinter as tk
from tkinter import ttk

def calcular_preco_venda(custo_fixo, rendimento_mensal, custo_operacional, impostos, comissao_venda, margem_lucro):
    try:
        custo_fixo = float(custo_fixo)
        rendimento_mensal = float(rendimento_mensal)
        custo_operacional = float(custo_operacional)
        impostos = float(impostos)
        comissao_venda = float(comissao_venda)
        margem_lucro = float(margem_lucro)

        # Calcular o preço de venda
        preco_venda = rendimento_mensal / (1 - (impostos + custo_fixo + custo_operacional + margem_lucro + comissao_venda) / 100)

        # Atualizar o campo de preço de venda na tela principal
        entry_preco_venda.delete(0, tk.END)
        entry_preco_venda.insert(0, f"{preco_venda:.2f}")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

def calcular_custo_fixo(rendimento_mensal, custo_fixo, entry_percentual_custo_fixo):
    try:
        rendimento_mensal = float(rendimento_mensal)
        custo_fixo = float(custo_fixo)
        
        # Calcular o percentual do custo fixo em relação ao rendimento mensal
        percentual_custo_fixo = (custo_fixo / rendimento_mensal) * 100
        
        # Atualizar o campo de custo fixo na tela principal
        entry_percentual_custo_fixo.delete(0, tk.END)
        entry_percentual_custo_fixo.insert(0, f"{percentual_custo_fixo:.2f}%")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")


def tela_calculo_venda():
    # Crie uma nova janela
    nova_janela = tk.Toplevel(root)
    nova_janela.title("Calculadora de Preço de Venda")

    # Adicione conteúdo à nova janela
    frame = ttk.Frame(nova_janela, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    label_percentual_custo_fixo = ttk.Label(frame, text="Percentual do Custo Fixo:")
    label_percentual_custo_fixo.grid(row=0, column=0, sticky=tk.W)
    entry_percentual_custo_fixo = ttk.Entry(frame, width=15)
    entry_percentual_custo_fixo.grid(row=0, column=1, sticky=tk.W)

    # Campos de entrada
    label_rendimento_mensal = ttk.Label(frame, text="Rendimento bruto Mensal:")
    label_rendimento_mensal.grid(row=0, column=0, sticky=tk.W)
    entry_rendimento_mensal = ttk.Entry(frame, width=15)
    entry_rendimento_mensal.grid(row=0, column=1, sticky=tk.W)

    label_custo_fixo = ttk.Label(frame, text="Custo Fixo:")
    label_custo_fixo.grid(row=1, column=0, sticky=tk.W)
    entry_custo_fixo = ttk.Entry(frame, width=15)
    entry_custo_fixo.grid(row=1, column=1, sticky=tk.W)

    # Botão para calcular o custo fixo
    botao_calcular_custo_fixo = ttk.Button(frame, text="Calcular Custo Fixo",
                                       command=lambda: calcular_custo_fixo(entry_rendimento_mensal.get(),
                                                                          entry_custo_fixo.get(),
                                                                          entry_percentual_custo_fixo))

    botao_calcular_custo_fixo.grid(row=2, columnspan=2, pady=10)
    label_custo_operacional = ttk.Label(frame, text="Custo Operacional (% do rendimento mensal):")
    label_custo_operacional.grid(row=2, column=0, sticky=tk.W)
    entry_custo_operacional = ttk.Entry(frame, width=15)
    entry_custo_operacional.grid(row=2, column=1, sticky=tk.W)

    label_impostos = ttk.Label(frame, text="Impostos (%):")
    label_impostos.grid(row=3, column=0, sticky=tk.W)
    entry_impostos = ttk.Entry(frame, width=15)
    entry_impostos.grid(row=3, column=1, sticky=tk.W)

    label_comissao_venda = ttk.Label(frame, text="Comissão de Venda (%):")
    label_comissao_venda.grid(row=4, column=0, sticky=tk.W)
    entry_comissao_venda = ttk.Entry(frame, width=15)
    entry_comissao_venda.grid(row=4, column=1, sticky=tk.W)

    label_margem_lucro = ttk.Label(frame, text="Margem de Lucro (%):")
    label_margem_lucro.grid(row=5, column=0, sticky=tk.W)
    entry_margem_lucro = ttk.Entry(frame, width=15)
    entry_margem_lucro.grid(row=5, column=1, sticky=tk.W)

    # Botão para calcular o preço de venda
    botao_calcular = ttk.Button(frame, text="Calcular Preço de Venda",
                                command=lambda: calcular_preco_venda(entry_custo_fixo.get(),
                                                                       entry_rendimento_mensal.get(),
                                                                       entry_custo_operacional.get(),
                                                                       entry_impostos.get(),
                                                                       entry_comissao_venda.get(),
                                                                       entry_margem_lucro.get()))
    botao_calcular.grid(row=6, columnspan=2, pady=10)

def gerar_codigo_barra():
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
        if resultado > 0 :
            return gerar_codigo_barra()
    except:

        fc.limpar_tela()

    return codigo

def cadastrar_produto():
    # Obter os valores dos campos
    nome = entry_nome.get()
    descricao = entry_descricao.get()
    codigo_de_barras = gerar_codigo_barra()
    preco_de_compra = entry_custo_aquisicao.get()
    preco_de_venda = entry_preco_venda.get()
    unidades = entry_unidades.get()
    fornecedor = combo_fornecedor.get()

    # Validar os campos
    if not fc.validar_nvarchar2(nome,50,1):
        return
    if not fc.validar_nvarchar2(descricao,50,0):
        return
    if not fc.validar_number("preco de venda",preco_de_venda,1):
        return
    if not fc.validar_number("preço de compra",preco_de_compra,1):
        return
    if not fc.validar_number("unidades",unidades,1):
        return
    
    # converte os valores
    preco_de_venda = preco_de_venda.replace(',','.') # substitui a virgula pelo ponto antes de converter para float
    preco_de_venda = float(preco_de_venda)

    preco_de_compra = preco_de_compra.replace(',','.') 
    preco_de_compra = float(preco_de_venda)

    unidades = unidades.replace(',','.') 
    unidades = int(preco_de_venda)

   # adiciona ao banco de dados
    try:
        cursor.execute("""
        INSERT INTO tbl_produtos (nome, descricao, codigo_de_barras, preco_de_compra, preco_de_venda, unidades, fornecedor)
        VALUES (:nome, :descricao, :codigo_de_barras, :preco_de_compra, :preco_de_venda, :unidades, :fornecedor)
        """, {
        'nome': nome,
        'descricao': descricao,
        'codigo_de_barras': codigo_de_barras,
        'preco_de_compra': preco_de_compra,
        'preco_de_venda': preco_de_venda,
        'unidades': unidades,
        'fornecedor': fornecedor
        })

        connection.commit() # Salva as alterações no banco de dados

  

    except oracledb.DatabaseError as e:
        return


    # Aqui você pode adicionar mais validações para outros campos se necessário

    # Aqui você pode adicionar a lógica para salvar os dados do produto no banco de dados ou em algum arquivo

    # Limpar campos após o cadastro
    entry_nome.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    entry_custo_aquisicao.delete(0, tk.END)
    entry_preco_venda.delete(0, tk.END)
    entry_unidades.delete(0, tk.END)
    combo_fornecedor.set("")  # Limpar a seleção do fornecedor

    # Mostrar mensagem de sucesso
    messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")


# Configuração da janela principal
root = tk.Tk()
root.title("Cadastro de Produtos")

# Frame para agrupar os campos
frame = ttk.Frame(root, padding="20")
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

label_preco_venda = ttk.Label(frame, text="Preço de Venda:")
label_preco_venda.grid(row=5, column=0, sticky=tk.W)
entry_preco_venda = ttk.Entry(frame, width=50)
entry_preco_venda.grid(row=5, column=1, sticky=tk.W)

botao_nova_tela = ttk.Button(frame, text="Calcular Preço de venda", command=tela_calculo_venda)
botao_nova_tela.grid(row=5, column=2, padx=10, sticky=tk.W)


# Botão para cadastrar produto
button_cadastrar = ttk.Button(frame, text="Cadastrar Produto", command=cadastrar_produto)
button_cadastrar.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
