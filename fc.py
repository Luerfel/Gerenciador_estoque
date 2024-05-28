import os
import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import oracledb


def conectar_banco():
 # **Observações:**
# Este código utiliza um banco de dados local para armazenar as informações.
# Altere as variáveis `user`, `password`, `host`, `port` para conectar-se ao seu banco de dados.

# **Detalhes da conexão:**
# * **user:** Nome de usuário do banco de dados.
# * **password:** Senha do banco de dados.
# * **host:** Nome do serviço do banco de dados.
# * **port:** Porta do serviço do banco de dados.

    try:
        return oracledb.connect(user="SYSTEM", password="testador", host="localhost", port=1521)
    except oracledb.DatabaseError as e:
        messagebox.showerror("Erro de conexão", f"Não foi possível conectar ao banco de dados: {e}")
        return None

def limpar_tela():
    # Usado para a limpeza da tela do sistema operacional windowns e linux.
    if os.name == 'nt':
        os.system('cls')  # windowns
    else:
        os.system('clear')  # linux

def validar_nvarchar2(campo, tam, not_null):
    """
    valida se o dado nvarchar2  está dentro dos critérios.
    recebe tamanho para fazer a verificação se ultrapassa o tamanho maximo.
    o nome do dado, e not_null se for igual a 1 significado que é um campo obrigatório

    Retorna:
    str: O dado.

    """
    if not_null == 1:
        if not campo:
            messagebox.showerror("Erro", "Por favor, preencha o campo 'Nome'.")
            return False
    
    if len(campo) > tam:
        messagebox.showerror("Erro", f"O campo {campo} deve ter no máximo {tam} caracteres.")
        return False

    return True

def validar_number(campo, valor, not_null):
    """
    valida se o dado number  está dentro dos critérios.

    o nome do dado, e not_null se for igual a 1 significado que é um campo obrigatório

    Retorna:
    TRUE se atender todos os critérios
    """
    valor = valor.replace(',', '.')  # substitui a virgula pelo ponto antes de converter para float

    if not_null == 1:
        if not valor:
            messagebox.showerror("Erro", f"Por favor, preencha o campo '{campo}'.")
            return False
    try:
        numero = float(valor)
    except ValueError:
        messagebox.showerror("Erro", f"O campo '{campo}' deve ser um número.")
        return False

    return True

def calcular_custos_e_percentuais(entry_rendimento_mensal, entry_custo_fixo, entry_custo_mercadoria,
                                  entry_custo_operacional, entry_percentual_custo_fixo,
                                  entry_percentual_custo_operacional):
    """
    Calcula e exibe os percentuais de custos fixos e operacionais em relação ao rendimento mensal
    e ao custo total das mercadorias, respectivamente.

    Args:
        entry_rendimento_mensal (tk.Entry): Entry widget para o rendimento mensal.
        entry_custo_fixo (tk.Entry): Entry widget para o custo fixo.
        entry_custo_mercadoria (tk.Entry): Entry widget para o custo total das mercadorias.
        entry_custo_operacional (tk.Entry): Entry widget para o custo operacional.
        entry_percentual_custo_fixo (tk.Entry): Entry widget para exibir o percentual do custo fixo.
        entry_percentual_custo_operacional (tk.Entry): Entry widget para exibir o percentual do custo operacional.
    """

    def calcular_e_exibir_percentual(referencia, custo, entry_resultado, tipo):
        try:
            valor_referencia = float(referencia.get())
            valor_custo = float(custo.get())
            percentual = (valor_custo / valor_referencia) * 100
            entry_resultado.configure(state="normal")
            entry_resultado.delete(0, ctk.END)
            entry_resultado.insert(0, "{:.2f}".format(percentual))
            entry_resultado.configure(state="readonly")
        except ValueError:
            entry_resultado.configure(state="normal")
            entry_resultado.delete(0, ctk.END)
            entry_resultado.insert(0, "Erro")
            entry_resultado.configure(state="readonly")

    # Calcular e exibir percentuais
    calcular_e_exibir_percentual(entry_rendimento_mensal, entry_custo_fixo, entry_percentual_custo_fixo,
                                 "rendimento mensal")
    calcular_e_exibir_percentual(entry_custo_mercadoria, entry_custo_operacional, entry_percentual_custo_operacional,
                                 "custo total das mercadorias")

def key_matriz():
    return  [ [3,3],[2,5]]
        