import oracledb # biblioteca da oracle
import os      # usado na limpeza da tela
import random
import fc
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

taxas = 1


# Programa principal
def main ():
    while True:
        repeticao = 1
        print("\n--- Menu de Cadastro de Produtos ---")
        print("2. Exibir Tabelas")
        print("3. Criar tabela (use caso seja um novo banco de dados)")
        print("0. Sair")
        while repeticao == 1:
            try:
             opcao = int(input("Digite a opção desejada: "))
             fc.limpar_tela()
             repeticao = 0
            except:
                print("ERRO! TENTE NOVAMENTE!")
        if opcao == 1:
            cadastrar_produto()
        elif opcao == 2:
            imprimir_tabela()
        elif opcao == 0:
            print("Saindo do programa...")
            return
        elif opcao == 3:
            criar_tabela()
        else:
            print("Opção inválida! Tente novamente.")

# FUNÇÕES

def criar_tabela():
    try:

        cursor.execute("""
        CREATE TABLE tbl_produtos (
            nome NVARCHAR2(100),
            descricao NVARCHAR2(255),
            codigo_de_barras NVARCHAR2(13) PRIMARY KEY,
            preco_de_compra NUMBER(10,2),
            preco_de_venda NUMBER(10,2),
            unidades INT,
            fornecedor NVARCHAR2(100)
        )
        """)
        connection.commit() # Salva as alterações no banco de dados
        print("Tabela Criada com sucesso!!")
    except oracledb.DatabaseError as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return
    

def cadastrar_produto():

    """
    Função para cadastrar um novo produto no banco de dados.

    Essa função solicita ao usuário os dados do produto e os insere na tabela `tbl_produtos`.
    """


    # Solicitação dos dados do produto

  
    # Nome do produto
    nome = fc.dado_nvarchar2(100, "o nome", 1)

    # Descrição do produto
    descricao = fc.dado_nvarchar2(255, "a descrição", 0)

    # Geração do código de barras
    codigo_de_barras = gerar_codigo_barra()

    # Preço de compra do produto
    preco_de_compra = fc.dado_number(13, "o preco de compra")

    # Cálculo do preço de venda
    preco_de_venda = fc.calcular_preco_venda(preco_de_compra, taxas, 20)

    # Quantidade de unidades do produto
    unidades = int(fc.dado_number(13, "unidades"))

    # Nome do fornecedor do produto
    fornecedor = fc.dado_nvarchar2(100, "O Fornecedor",0)



  # Inserção do produto no banco de dados

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

        print("Produto cadastrado com sucesso!")
        input = ("Pressione ENTER para continuar.\n ")
        fc.limpar_tela()

    except oracledb.DatabaseError as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return

def imprimir_tabela():
    for row in cursor.execute('SELECT * FROM tbl_produtos'):
        print(f"""
Nome: {row[0]}
Descrição: {row[1]}
Código de Barras: {row[2]}
Preço de Compra: R${row[3]:.2f}
Preço de Venda: R${row[4]:.2f}
Unidades: {row[5]}
Fornecedor: {row[6]}
""")
    input("Aperte ENTER para continuar!\n")
    fc.limpar_tela()

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

if __name__ == "__main__":
    main()

connection.close() # finaliza a  conexão com o banco de dados
