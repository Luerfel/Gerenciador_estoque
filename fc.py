import os
import random
import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk


def calcular_preco_venda(entry_preco_venda_principal,entry_preco_venda,entry_custo_imposto, entry_margem_lucro, entry_comissao_venda, entry_custo_produto, entry_percentual_custo_fixo, entry_percentual_custo_operacional):
        ca = float(entry_custo_produto.get())
        iv = float(entry_custo_imposto.get())
        cf = float(entry_percentual_custo_fixo.get())
        co = float(entry_percentual_custo_operacional.get())
        ml = float(entry_margem_lucro.get())
        cv = float(entry_comissao_venda.get())
        preco_venda = ca / (1 - ((iv + cf + co + ml + cv) / 100))
        try:
            entry_preco_venda.configure(state="normal")
            entry_preco_venda.delete(0, tk.END)
            entry_preco_venda.insert(0, "{:.2f}".format(preco_venda))
            entry_preco_venda.configure(state="readonly") 
        except:
            entry_preco_venda.configure(state="normal")
            entry_preco_venda.delete(0, tk.END)
            entry_preco_venda.insert(0, "Erro")
            entry_preco_venda.configure(state="readonly")

def limpar_tela():
    # Usado para a limpeza da tela do sistema operacional windowns e linux.
    if os.name == 'nt':
        os.system('cls')  # windowns
    else:
        os.system('clear')  # linux


def dado_number(tamanho, nome):
    """
    Leitura de dados do tipo float.

    Retorna:
    str: dado float.
    """
    repeticao = 1

    while repeticao == 1:
        try:
            dado = float(input(f"Digite {nome} do produto : "))
            limpar_tela()
            # número válido
            repeticao = 0

        except ValueError:
            print(f"ERRO: {nome} inválido. Digite um número.")

        except NameError as e:
            print(f"ERRO: {e}")

        except OverflowError:
            print(f"Erro: {nome} muito grande. Digite um número menor.")

    return dado



    # Converte a margem de lucro em porcentagem p


def dado_nvarchar2(tamanho, nome, not_null):
    """
    Lê Dado do tipo nvarchar2 e valida se ele está dentro dos critérios.
    recebe tamanho para fazer a verificação se ultrapassa o tamanho maximo.
    o nome do dado, e not_null se for igual a 1 significado que é um campo obrigatório

    Retorna:
    TRUE se atender todos os critérios

    """
    repeticao = 1
    while (repeticao == 1):

        try:
            dado = input(f"Digite {nome} do produto : ")
            limpar_tela()

            # validação de tamanho
            if len(dado) >= tamanho:
                raise ValueError(f"Use no máximo {tamanho} caracteres.")

            # verifica se a string esta vazia
            elif len(dado) <= 0 and not_null == 1:
                raise NameError("Campo Obrigatório!!")

            else:
                # Nome válido
                repeticao = 0

        except ValueError as e:
            print("ERRO : ", e)

        except NameError as e:
            print("ERRO :", e)

        except:
            print("ERRO!")

    return dado


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
        messagebox.showerror(f"Erro", "O campo {campo} deve ter no máximo {tam} caracteres.")
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

