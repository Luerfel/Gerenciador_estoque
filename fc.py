import os
import random


def limpar_tela():
    # Usado para a limpeza da tela do sistema operacional windowns e linux.
    if os.name =='nt':
        os.system('cls') # windowns
    else:
        os.system('clear') # linux

def dado_number(tamanho,nome):
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
            print (f"ERRO: {nome} inválido. Digite um número.")

        except NameError as e:
            print(f"ERRO: {e}")

        except OverflowError:
            print(f"Erro: {nome} muito grande. Digite um número menor.")


    return dado

def calcular_preco_venda(custo_produto, taxas_venda, margem_lucro):
  """
  Calcula o preço de venda de um produto, quando tiver a interface iremos adaptar para que o,
  usuário tenha mais possibilidade

  Argumentos:
    custo_produto (float): Custo do produto.
    taxas_venda (float): Taxas de venda (ex: imposto, frete).
    margem_lucro (float): Margem de lucro desejada (ex: 0.2 para 20%).

    

  Retorna:
    float: Preço de venda calculado.
  """

  # Converte a margem de lucro em porcentagem para um valor decimal
  margem_lucro_decimal = margem_lucro / 100

  # Calcula o lucro desejado
  lucro_desejado = custo_produto * margem_lucro_decimal

  # Soma as taxas de venda ao custo do produto
  custo_total = custo_produto + taxas_venda

  # Calcula o preço de venda
  preco_venda = custo_total / (1 - margem_lucro_decimal)

  return preco_venda

def dado_nvarchar2(tamanho,nome,not_null):
    """
    Lê Dado do tipo nvarchar2 e valida se ele está dentro dos critérios.
    recebe tamanho para fazer a verificação se ultrapassa o tamanho maximo.
    o nome do dado, e not_null se for igual a 1 significado que é um campo obrigatório

    Retorna:
    str: O dado.

    """
    repeticao = 1
    while(repeticao == 1):
    
        try:
            dado = input(f"Digite {nome} do produto : ")
            limpar_tela()

            # validação de tamanho
            if   len(dado) >= tamanho:
                raise ValueError(f"Use no máximo {tamanho} caracteres.")
            
            # verifica se a string esta vazia
            elif len(dado) <= 0 and not_null == 1:
                raise NameError("Campo Obrigatório!!")
        
            else:
                # Nome válido 
                repeticao = 0

        except ValueError as e:
            print("ERRO : ",e)

        except NameError as e:
            print ("ERRO :",e)

        except:
            print("ERRO!")

    return dado