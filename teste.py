import tkinter as tk
from tkinter import ttk

def calcular_porcentagem_custo_fixo(entry_rendimento_mensal, entry_custo_fixo, entry_percentual_custo_fixo):
    try:
        rendimento_mensal = float(entry_rendimento_mensal.get())
        custo_fixo = float(entry_custo_fixo.get())
        percentual_custo_fixo = (custo_fixo / rendimento_mensal) * 100
        entry_percentual_custo_fixo.config(state="normal")
        entry_percentual_custo_fixo.delete(0, tk.END)
        entry_percentual_custo_fixo.insert(0, "{:.2f}".format(percentual_custo_fixo))
        entry_percentual_custo_fixo.config(state="readonly")
        # Limpar campos após cálculo
        entry_rendimento_mensal.delete(0, tk.END)
        entry_custo_fixo.delete(0, tk.END)
    except ValueError:
        # Se valores inseridos não forem números
        entry_percentual_custo_fixo.config(state="normal")
        entry_percentual_custo_fixo.delete(0, tk.END)
        entry_percentual_custo_fixo.insert(0, "Erro")
        entry_percentual_custo_fixo.config(state="readonly")

def tela_calculo_venda():
    # Crie uma nova janela
    nova_janela = tk.Toplevel(root)
    nova_janela.title("Calculadora de Preço de Venda")
    nova_janela.geometry("600x600")

    # Adicione conteúdo à nova janela
    frame = ttk.Frame(nova_janela, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Percentual do custo fixo
    label_percentual_custo_fixo = ttk.Label(frame, text="Percentual do Custo Fixo:")
    label_percentual_custo_fixo.grid(row=3, column=0, sticky=tk.W)
    entry_percentual_custo_fixo = ttk.Entry(frame, width=15, state="readonly")
    entry_percentual_custo_fixo.grid(row=3, column=1, sticky=tk.W)

    label_rendimento_mensal = ttk.Label(frame, text="Rendimento bruto Mensal:")
    label_rendimento_mensal.grid(row=0, column=0, sticky=tk.W)
    entry_rendimento_mensal = ttk.Entry(frame, width=15)
    entry_rendimento_mensal.grid(row=0, column=1, sticky=tk.W)

    label_custo_fixo = ttk.Label(frame, text="Custo Fixo:")
    label_custo_fixo.grid(row=1, column=0, sticky=tk.W)
    entry_custo_fixo = ttk.Entry(frame, width=15)
    entry_custo_fixo.grid(row=1, column=1, sticky=tk.W)

    # Botão para calcular o percentual do custo fixo
    btn_calcular = ttk.Button(frame, text="Calcular Percentual do custo fixo", command=lambda: calcular_porcentagem_custo_fixo(entry_rendimento_mensal, entry_custo_fixo, entry_percentual_custo_fixo))
    btn_calcular.grid(row=2, columnspan=2, pady=10)

    # custo operacional

    label_percentual_custo_operacional = ttk.Label(frame, text="Percentual do Custo Fixo:")
    label_percentual_custo_operacional.grid(row=3, column=0, sticky=tk.W)
    entry_percentual_custo_operacional = ttk.Entry(frame, width=15, state="readonly")
    entry_percentual_custo_operacional.grid(row=3, column=1, sticky=tk.W)

    label_custo_mercadoria = ttk.Label(frame, text="Custo total das Mercadorias:")
    label_custo_mercadoria.grid(row=0, column=0, sticky=tk.W)
    entry_custo_mercadoria = ttk.Entry(frame, width=15)
    entry_custo_mercadoria.grid(row=0, column=1, sticky=tk.W)

    label_custo_fixo = ttk.Label(frame, text="Custo Fixo:")
    label_custo_fixo.grid(row=1, column=0, sticky=tk.W)
    entry_custo_fixo = ttk.Entry(frame, width=15)
    entry_custo_fixo.grid(row=1, column=1, sticky=tk.W)

    # Botão para calcular o percentual do custo fixo
    btn_calcular = ttk.Button(frame, text="Calcular Percentual do custo fixo", command=lambda: calcular_porcentagem_custo_fixo(entry_rendimento_mensal, entry_custo_fixo, entry_percentual_custo_fixo))
    btn_calcular.grid(row=2, columnspan=2, pady=10)




# Criar a janela principal
root = tk.Tk()
tela_calculo_venda()
root.mainloop()
