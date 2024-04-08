import tkinter as tk
from tkinter import ttk

def salvar_preco_venda(preco_venda, label_preco_venda_principal):
    label_preco_venda_principal.config(text=f"Preço de Venda: {preco_venda}")

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

def calcular_preco_venda(ca, entry_iv, entry_cf, entry_co, entry_ml, entry_cv, entry_preco_venda):

    ca = float(ca)
    print(ca," Custo do produto")
    iv = float(entry_iv.get())
    print(iv," Imposto")
    cf = float(entry_cf.get())
    print(cf,"custo fixo")
    co = float(entry_co.get())
    print(co , "custo operacionail")
    ml = float(entry_ml.get())
    print(ml," Margem lucro")
    cv = float(entry_cv.get())
    print(cv , "preço venda")
    preco_venda = ca / (1 - (iv + cf + co + ml + cv) / 100)
    try:    
        entry_preco_venda.config(state="normal")
        entry_preco_venda.delete(0, tk.END)
        entry_preco_venda.insert(0, "{:.2f}".format(preco_venda))
        entry_preco_venda.config(state="readonly")
    except:
        entry_preco_venda.config(state="normal")
        entry_preco_venda.delete(0, tk.END)
        entry_preco_venda.insert(0, "Erro")
        entry_preco_venda.config(state="readonly")
    

def tela_calculo_venda():
    # Crie uma nova janela
    nova_janela = tk.Toplevel(root)
    nova_janela.title("Calculadora de Preço de Venda")

    # Adicione conteúdo à nova janela
    frame = ttk.Frame(nova_janela, padding="20")
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
                              command=lambda: calcular_percentuais(entry_rendimento_mensal, entry_custo_fixo, entry_custo_mercadoria, entry_custo_operacional, entry_percentual_custo_fixo, entry_percentual_custo_operacional))
    btn_calcular.grid(row=3, columnspan=4, pady=10)
    
    # impostos
    label_custo_imposto = ttk.Label(frame, text="Percentual do imposto:")
    label_custo_imposto.grid(row=7, column=0, sticky=tk.W)
    entry_custo_imposto = ttk.Entry(frame, width=15)
    entry_custo_imposto.grid(row=7, column=1, sticky=tk.W)

   # comissão de venda
    label_comissao_venda = ttk.Label(frame, text="Percentual da Comissão Venda:")
    label_comissao_venda.grid(row=8, column=0, sticky=tk.W)
    entry_comissao_venda = ttk.Entry(frame, width=15)
    entry_comissao_venda.grid(row=8, column=1, sticky=tk.W)
   
   # Margem de lucro
    label_margem_lucro = ttk.Label(frame, text="Percentual da Margem de Lucro:")
    label_margem_lucro.grid(row=9, column=0, sticky=tk.W)
    entry_margem_lucro = ttk.Entry(frame, width=15)
    entry_margem_lucro.grid(row=9, column=1, sticky=tk.W)

    label_preco_venda = ttk.Label(frame, text="Preço de Venda:")
    label_preco_venda.grid(row=10, column=0, sticky=tk.W)
    entry_preco_venda = ttk.Entry(frame, width=15, state="readonly")
    entry_preco_venda.grid(row=10, column=1, sticky=tk.W)
    ca = "10"
    btn_calcular = ttk.Button(frame, text="Calcular preço de venda",
                              command=lambda: calcular_preco_venda(ca, entry_custo_imposto, entry_percentual_custo_fixo, entry_percentual_custo_operacional, entry_margem_lucro, entry_comissao_venda, entry_preco_venda))
    btn_calcular.grid(row=11, columnspan=4, pady=10)

    # Botão "Salvar"
    btn_salvar = ttk.Button(frame, text="Salvar", command=lambda: salvar_preco_venda(entry_preco_venda.get(), label_preco_venda_principal))
    btn_salvar.grid(row=14, columnspan=4, pady=10)



    entry_preco_venda.get()


def calcular_percentuais(entry_rendimento_mensal, entry_custo_fixo, entry_custo_mercadoria, entry_custo_operacional, entry_percentual_custo_fixo, entry_percentual_custo_operacional):
    # função auxiliar para o calcular_porcentagem_custo fazer o calculo 2x
    calcular_porcentagem_custo(entry_rendimento_mensal, entry_custo_fixo, entry_percentual_custo_fixo, "rendimento mensal")
    calcular_porcentagem_custo(entry_custo_mercadoria, entry_custo_operacional, entry_percentual_custo_operacional, "custo total das mercadorias")

# Criar a janela principal
root = tk.Tk()
tela_calculo_venda()
label_preco_venda_principal = ttk.Label(root, text="")
label_preco_venda_principal.pack()

root.mainloop()
