import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
import customtkinter as ctk
import oracledb
import subprocess
from datetime import datetime
import fc
from tkcalendar import DateEntry

class MainScreen:
    """
    Classe para a tela principal do sistema de gerenciamento de estoque.
    """

    def __init__(self, root_parameter):
        """
        Inicializa a tela principal.

        Args:
            root_parameter (tk.Tk): A janela principal do aplicativo.
        """
        self.root = root_parameter
        self.montar_tela_principal()
        self.ajustar_grid()
        self.buttons_design()
        self.listar_produtos()
        self.entry_info()
        self.criar_label_total()
        self.setup_bindings()
        self.connection = fc.conectar_banco()
        self.root.protocol("WM_DELETE_WINDOW", self.confirm_exit)
        if self.connection:
            self.cursor = self.connection.cursor()
        else:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            self.root.destroy()
        self.root.mainloop()



    def ajustar_grid(self):
        """
        Ajusta a configuração da grade da janela principal.
        """
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=6)
        self.root.grid_rowconfigure(2, weight=6)
        self.root.grid_columnconfigure(0, weight=6)
        self.root.grid_columnconfigure(1, weight=3)

    def montar_tela_principal(self):
        """
        Configura a aparência da tela principal.
        """
        self.root.geometry("1200x720")
        self.root.title("Stock Management System")
        self.root.resizable(False, False)
        self.root.configure(background="#f9f6ee")

    def setup_bindings(self):
        """
        Configura os atalhos de teclado.
        """
        self.root.bind("<F1>", self.cadastrar_produto)
        self.root.bind("<F2>", self.consultar_produto)
        self.root.bind("<F3>", self.editar_produto)
        self.root.bind("<F4>", self.excluir_produto)
        self.root.bind("<F5>", self.cadastrar_fornecedor)
        self.root.bind("<F6>", self.limpar_tela)
        self.root.bind("<F7>", self.concluir_venda)  
        self.root.bind("<F8>", self.consultar_vendas)



    def buttons_design(self):
        """
        Cria e estiliza os botões na tela principal.
        """
        self.buttons_container = ctk.CTkFrame(self.root, fg_color="#242424")
        self.buttons_container.grid(row=0, column=0, columnspan=12, padx=20, pady=20, sticky="nsew")
        button_data = [
            ("F1\nCadastrar Produto", 0, 0, self.cadastrar_produto),
            ("F2\nConsultar Produto", 0, 1, self.consultar_produto),
            ("F3\nEditar Produto", 0, 2, self.editar_produto),
            ("F4\nExcluir Produto", 0, 3, self.excluir_produto),
            ("F5\nCadastrar Fornecedor", 0, 4, self.cadastrar_fornecedor),  
            ("F6\nCancelar Venda", 0, 5, self.limpar_tela),
            ("F7\nConcluir Venda", 0, 6, self.concluir_venda),  
            ("F8\nConsultar Vendas", 0, 7, self.consultar_vendas)

        ]
        for text, row, column, command in button_data:
            button = ctk.CTkButton(self.buttons_container, text=text, width=80, height=40, corner_radius=13)
            button.grid(row=row, column=column, padx=10, pady=10)
            button.configure(hover_color="#5662f6", cursor="hand2")
            if command:
                button.bind("<Button-1>", command)

    def cadastrar_produto(self, event=None):
        """
        Abre o arquivo de cadastro de produto.
        """
        subprocess.Popen(["python", "cadastrar_produto.py"])

    def consultar_produto(self, event=None):
        """
        Abre o arquivo de consulta de produto.
        """
        subprocess.Popen(["python", "consultar_produto.py"])

    def editar_produto(self, event=None):
        """
        Abre o arquivo de edição de produto.
        """
        subprocess.Popen(["python", "editar_produto.py"])

    def excluir_produto(self, event=None):
        """
        Abre o arquivo de exclusão de produto.
        """
        subprocess.Popen(["python", "excluir_produto.py"])
    
    def cadastrar_fornecedor(self, event=None):
        """
        Abre o arquivo de exclusão de produto.
        """
        subprocess.Popen(["python", "cadastrar_fornecedor.py"])

    def buscar_produto(self):
        """
        Busca um produto pelo código de barras.
        """
        termo_busca = self.entry_busca.get()
        try:
            sql = "SELECT nome, preco_de_venda FROM tbl_produtos WHERE codigo_de_barras = :TERMOS_BUSCA"
            self.cursor.execute(sql, {"TERMOS_BUSCA": termo_busca})
            resultado = self.cursor.fetchone()
            if resultado:
                nome, preco_venda = resultado
                self.nome_entry.configure(state=tk.NORMAL)
                self.unitario_entry.configure(state=tk.NORMAL)
                self.nome_entry.delete(0, tk.END)
                self.nome_entry.insert(0, nome)
                self.unitario_entry.delete(0, tk.END)
                self.unitario_entry.insert(0, f"R$ {preco_venda:.2f}")
                self.nome_entry.configure(state='readonly')
                self.unitario_entry.configure(state='readonly')
                self.quantidade_entry.delete(0, tk.END)
                self.quantidade_entry.insert(0, "1")
                self.calcular_total(None)
            else:
                messagebox.showerror("Erro", "Produto não encontrado.")
        except oracledb.DatabaseError as e:
            error, = e.args
            print(f"Erro ao buscar produto: {error.message}")
            messagebox.showerror("Erro de Banco de Dados", "Ocorreu um erro ao buscar o produto. Tente novamente.")

    def limpar_tela(self, event=None):
        """
        Limpa a tela e cancela a venda atual.
        """
        resposta = messagebox.askyesno("Cancelar Venda", "Tem certeza que deseja cancelar a venda atual? Todos os itens serão removidos.")
        if resposta:
            self.entry_busca.delete(0, ctk.END)
            self.nome_entry.delete(0, ctk.END)
            self.unitario_entry.delete(0, ctk.END)
            self.quantidade_entry.delete(0, ctk.END)
            self.total_entry.delete(0, ctk.END)
            self.tree.delete(*self.tree.get_children())
            self.label_total.configure(text="Valor Total : R$ 0.00")
            self.limpar_campos()

    def listar_produtos(self):
        """
        Exibe uma lista de produtos na tela principal.
        """
        # configuração da tela
        style = ttk.Style()
        style.configure("Treeview",
                    background="#f0f0f0",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#f0f0f0",
                    font=("arial", 11))
        style.map('Treeview', background=[('selected', '#347083')])
    
        # Alternar as cores das linhas
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
   

        # Frame para conter a Treeview e a barra de rolagem
        tree_frame = ctk.CTkFrame(self.root)
        tree_frame.grid(row=1, column=1, padx=20, pady=20, sticky='nsew')
    
        # Barra de rolagem vertical
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        vsb.pack(side='right', fill='y')
    
    
        self.tree = ttk.Treeview(tree_frame, columns=('col2', 'col3', 'col4', 'col5'), show='headings',
                             height=20, yscrollcommand=vsb.set, style="Treeview")

    
        vsb.config(command=self.tree.yview)
    
        # Definindo as colunas
        self.tree.column('col2', minwidth=0, width=100, anchor='center')
        self.tree.column('col3', minwidth=0, width=150, anchor='center')
        self.tree.column('col4', minwidth=0, width=50, anchor='center')
        self.tree.column('col5', minwidth=0, width=100, anchor='center')
    
        # Definindo os cabeçalhos
        self.tree.heading('col2', text='Código de Barra')
        self.tree.heading('col3', text='Nome Produto')
        self.tree.heading('col4', text='Quantidade')
        self.tree.heading('col5', text='Valor Total')
    
        # Empacotando a Treeview
        self.tree.pack(fill='both', expand=True)
    
        # Estilo para alternar cores de linhas
        self.tree.tag_configure('evenrow', background="lightblue")

    def entry_info(self):
        """
        Cria e estiliza os campos de entrada de informações.
        """
        container = ctk.CTkFrame(self.root, fg_color="#242424", corner_radius=22)
        container.grid(row=1, column=0, padx=20, pady=10, sticky='w')

        label_busca = ctk.CTkLabel(container, text="Código de Barras", bg_color="#242424")
        label_busca.grid(row=0, column=0, padx=(10, 5), pady=5, sticky='w')
        self.entry_busca = ctk.CTkEntry(container, bg_color="#2b2b2b")
        self.entry_busca.grid(row=0, column=1, padx=(0, 10), pady=5, sticky='ew')

        busca_button = ctk.CTkButton(container, text="Buscar", width=10, height=2, corner_radius=5, command=self.buscar_produto)
        busca_button.grid(row=0, column=2, padx=(10, 0), pady=10, sticky='w')
        busca_button.configure(hover_color="#5662f6", cursor="hand2")

        entry_data = [
            ("Nome", 1),
            ("Unitário R$", 2),
            ("Quantidade Total", 3),
            ("Total do Item R$", 4),
        ]
        for label_text, row in entry_data:
            label = ctk.CTkLabel(container, text=label_text, bg_color="#242424")
            label.grid(row=row, column=0, padx=(10, 5), pady=5, sticky='w')
            entry = ctk.CTkEntry(container, bg_color="#2b2b2b")
            entry.grid(row=row, column=1, padx=(0, 10), pady=5, sticky='ew')
            if label_text == "Nome":
                self.nome_entry = entry
                self.nome_entry.configure(state='readonly')
            elif label_text == "Unitário R$":
                self.unitario_entry = entry
                self.unitario_entry.configure(state='readonly')
            elif label_text == "Quantidade Total":
                self.quantidade_entry = entry
                self.quantidade_entry.bind("<FocusOut>", self.calcular_total)
                self.quantidade_entry.bind("<KeyRelease>", self.calcular_total)
            elif label_text == "Total do Item R$":
                self.total_entry = entry
                self.total_entry.configure(state='readonly')

        adicionar_button = ctk.CTkButton(container, text="Adicionar Item", width=10, height=2, corner_radius=5, command=self.adicionar_produto)
        adicionar_button.grid(row=5, column=1, padx=(10, 0), pady=10, sticky='w')
        adicionar_button.configure(hover_color="#5662f6", cursor="hand2")

    def calcular_total(self, event=None):
        """
        Calcula o total multiplicando o preço unitário pela quantidade total.
        """
        try:
            preco_unitario = float(self.unitario_entry.get().replace("R$", "").replace(",", "."))
            quantidade_total = float(self.quantidade_entry.get())
            total = preco_unitario * quantidade_total
            self.total_entry.configure(state=tk.NORMAL)
            self.total_entry.delete(0, tk.END)
            self.total_entry.insert(0, f"R$ {total:.2f}")
            self.total_entry.configure(state='readonly')
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido para quantidade ou preço unitário.")

    def adicionar_produto(self):
        """
        Adiciona um produto à lista de produtos.
        """
        codigo = self.entry_busca.get()
        if not codigo:
            messagebox.showerror("Erro", "Por favor, insira um código de barras válido.")
            return
        nome = self.nome_entry.get()
        if not nome:
            messagebox.showerror("Erro", "Por favor, busque um produto antes de adicioná-lo à lista.")
            return
        try:
            quantidade = int(self.quantidade_entry.get())
            valor_unitario = float(self.unitario_entry.get().replace("R$", "").replace(",", "."))
            valor_total = quantidade * valor_unitario
            self.tree.insert('', 'end', values=(codigo, nome, quantidade, f"R$ {valor_total:.2f}"))
            self.atualizar_valor_total()
            self.limpar_campos()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores válidos.")

    def limpar_campos(self):
        """
        Limpa os campos de entrada.
        """
        self.entry_busca.delete(0, tk.END)
        self.nome_entry.configure(state=tk.NORMAL)
        self.unitario_entry.configure(state=tk.NORMAL)
        self.total_entry.configure(state=tk.NORMAL)
        self.nome_entry.delete(0, tk.END)
        self.unitario_entry.delete(0, tk.END)
        self.quantidade_entry.delete(0, tk.END)
        self.total_entry.delete(0, tk.END)
        self.nome_entry.configure(state='readonly')
        self.unitario_entry.configure(state='readonly')
        self.total_entry.configure(state='readonly')

    def criar_label_total(self):
        """
        Cria uma label para mostrar o valor total de todos os itens.
        """
        self.label_total = ctk.CTkLabel(self.root, text="Valor Total : R$ 0.00", font=("Helvetica", 30))
        self.label_total.grid(row=2, column=1, padx=20, pady=10, sticky='w')

    def atualizar_valor_total(self):
        """
        Atualiza o valor total de todos os itens.
        """
        total = 0
        for child in self.tree.get_children():
            total += float(self.tree.item(child, 'values')[3].replace("R$", "").replace(",", ""))
        self.label_total.configure(text=f"Valor Total : R$ {total:.2f}")


    def concluir_venda(self, event=None):
        # Verifica se há itens na venda
        if not self.tree.get_children():
            messagebox.showwarning("Aviso", "Não há itens na venda.")
            return

        def salvar_venda():
            try:
                # Calcula o valor total da venda
                total_venda = calcular_total_venda()
                
                # Obtém e valida a forma de pagamento
                pagamento, forma_pagamento = obter_pagamento()
                if not validar_pagamento(pagamento, total_venda):
                    return
                
                # Obtém a data e horário atual
                data_venda, horario_venda = obter_data_horario_venda()
                
                # Insere a venda na tabela TBL_VENDAS e obtém o ID da venda
                venda_id = inserir_venda(data_venda, horario_venda, total_venda, forma_pagamento)
                
                # Insere os itens da venda na tabela TBL_ITENS_VENDA e atualiza o estoque
                inserir_itens_venda_e_atualizar_estoque(venda_id)
                
                # Confirma as mudanças no banco de dados
                self.connection.commit()
                
                # Conclui o processamento, limpando os campos e exibindo mensagem de sucesso
                concluir_processamento()
                
                # Fecha a janela de pagamento
                janela_pagamento.destroy()

            except ValueError as ve:
                messagebox.showerror("Erro de Pagamento", str(ve))
            except oracledb.DatabaseError as e:
                error, = e.args
                messagebox.showerror("Erro ao salvar venda", f"Ocorreu um erro ao salvar a venda: {error.message}")
                self.connection.rollback()

        def calcular_total_venda():
            # Calcula o valor total da venda somando os valores de todos os itens na árvore
            return sum(float(self.tree.item(item, 'values')[3].replace('R$', '').replace(',', '').strip()) for item in self.tree.get_children())

        def obter_pagamento():
            # Obtém os valores das entradas de pagamento
            pagamento = {
                'dinheiro': dinheiro_entry.get(),
                'pix': pix_entry.get(),
                'credito': credito_entry.get(),
                'debito': debito_entry.get()
            }
            
            # Identifica a forma de pagamento utilizada
            formas_pagamento = [k for k, v in pagamento.items() if v]
            
            # Se mais de uma forma de pagamento for usada, retorna erro
            if len(formas_pagamento) != 1:
                raise ValueError("Apenas uma forma de pagamento deve ser usada.")
            
            return pagamento, formas_pagamento[0]


        def validar_pagamento(pagamento, total_venda):
            # Verifica quantas formas de pagamento foram preenchidas
            formas_pagamento_usadas = [key for key, value in pagamento.items() if value]
            
            # Se mais de uma forma de pagamento for usada, mostra uma mensagem de erro e retorna
            if len(formas_pagamento_usadas) != 1:
                messagebox.showerror("Erro de Pagamento", "Apenas uma forma de pagamento deve ser usada.")
                return False

            # Converte os valores de pagamento para float e calcula o total do pagamento
            total_pagamento = 0
            for key in pagamento:
                if pagamento[key]:
                    try:
                        total_pagamento += float(pagamento[key].replace(',', '.'))
                    except ValueError:
                        messagebox.showerror("Erro de Formatação", f"O valor fornecido para {key} não é um número válido.")
                        return False

            # Verifica se o total do pagamento é igual ao valor total da venda
            if total_pagamento != total_venda:
                messagebox.showerror("Erro de Pagamento", "O valor pago deve ser exatamente igual ao valor total da venda.")
                return False

            return True

        def obter_data_horario_venda():
            # Obtém a data e o horário atual
            now = datetime.now()
            return now.date(), now.strftime("%H:%M:%S")

        def inserir_venda(data_venda, horario_venda, total_venda, formas_pagamento):
            # Insere a venda na tabela TBL_VENDAS
            sql_venda = """
            INSERT INTO TBL_VENDAS (DATA, horario, VALOR_TOTAL, FORMA_PAGAMENTO)
            VALUES (:1, :2, :3, :4)
            """
            self.cursor.execute(sql_venda, (data_venda, horario_venda, total_venda, formas_pagamento))
            self.connection.commit()
            
            # Obtém o ID da venda recém-inserida
            self.cursor.execute("SELECT ID FROM TBL_VENDAS WHERE ROWID = :1", [self.cursor.lastrowid])
            return self.cursor.fetchone()[0]

        def inserir_itens_venda_e_atualizar_estoque(venda_id):
            # Insere cada item da venda na tabela TBL_ITENS_VENDA e atualiza a quantidade na TBL_PRODUTOS
            for item in self.tree.get_children():
                codigo_de_barras = self.tree.item(item, 'values')[0]
                nome = self.tree.item(item, 'values')[1]
                quantidade = int(self.tree.item(item, 'values')[2])
                total_item = float(self.tree.item(item, 'values')[3].replace('R$', '').replace(',', '').strip())

                # Insere o item da venda na tabela TBL_ITENS_VENDA
                sql_item = """
                INSERT INTO TBL_ITENS_VENDA (VENDA_ID, CODIGO_PRODUTO, NOME_PRODUTO, QUANTIDADE, TOTAL_ITEM)
                VALUES (:1, :2, :3, :4, :5)
                """
                self.cursor.execute(sql_item, (venda_id, codigo_de_barras, nome, quantidade, total_item))

                # Atualiza a quantidade do produto na TBL_PRODUTOS
                sql_update_produto = """
                UPDATE TBL_PRODUTOS
                SET UNIDADES = UNIDADES - :1
                WHERE CODIGO_DE_BARRAS = :2
                """
                self.cursor.execute(sql_update_produto, (quantidade, codigo_de_barras))

        def concluir_processamento():
            # Exibe uma mensagem de sucesso e limpa a tela
            messagebox.showinfo("Venda Concluída", "Venda realizada com sucesso!")
            self.entry_busca.delete(0, ctk.END)
            self.nome_entry.delete(0, ctk.END)
            self.unitario_entry.delete(0, ctk.END)
            self.quantidade_entry.delete(0, ctk.END)
            self.total_entry.delete(0, ctk.END)
            self.tree.delete(*self.tree.get_children())
            self.label_total.configure(text="Valor Total : R$ 0.00")
            self.limpar_campos()

        # Cria uma janela para selecionar a forma de pagamento
        janela_pagamento = ctk.CTkToplevel(self.root)
        janela_pagamento.title("Forma de Pagamento")

        # Campos de entrada para diferentes formas de pagamento
        ctk.CTkLabel(janela_pagamento, text="Dinheiro").pack(pady=5)
        dinheiro_entry = ctk.CTkEntry(janela_pagamento)
        dinheiro_entry.pack(pady=5)

        ctk.CTkLabel(janela_pagamento, text="PIX").pack(pady=5)
        pix_entry = ctk.CTkEntry(janela_pagamento)
        pix_entry.pack(pady=5)

        ctk.CTkLabel(janela_pagamento, text="Cartão de Crédito").pack(pady=5)
        credito_entry = ctk.CTkEntry(janela_pagamento)
        credito_entry.pack(pady=5)

        ctk.CTkLabel(janela_pagamento, text="Cartão de Débito").pack(pady=5)
        debito_entry = ctk.CTkEntry(janela_pagamento)
        debito_entry.pack(pady=5)

        # Botões para salvar a venda ou cancelar
        salvar_button = ctk.CTkButton(janela_pagamento, text="Salvar Venda", command=salvar_venda)
        salvar_button.pack(pady=20)

        cancelar_button = ctk.CTkButton(janela_pagamento, text="Cancelar", command=janela_pagamento.destroy)
        cancelar_button.pack(pady=10)
    
    def consultar_vendas(self, event=None):
        # Função para fechar o caixa e exibir as vendas do dia

        # Cria uma nova janela para exibir as vendas do dia
        janela_caixa = ctk.CTkToplevel(self.root)
        janela_caixa.title("Fechar Caixa")

        # Traz a nova janela para frente e dá o foco
        janela_caixa.focus_force()

        # Frame para a seleção de data e a tabela de vendas
        frame_vendas = ctk.CTkFrame(janela_caixa)
        frame_vendas.pack(fill="both", expand=True, padx=10, pady=10)

        # Seletor de data
        label_data = ctk.CTkLabel(frame_vendas, text="Selecione a Data:")
        label_data.pack(pady=5)
        data_entry = DateEntry(frame_vendas, date_pattern="yyyy-mm-dd")
        data_entry.pack(pady=5)

        # Tabela para exibir as vendas
        tree_vendas = ttk.Treeview(frame_vendas, columns=("ID", "Data", "Horário", "Valor Total", "Forma de Pagamento"), show="headings")
        tree_vendas.heading("ID", text="ID")
        tree_vendas.heading("Data", text="Data")
        tree_vendas.heading("Horário", text="Horário")
        tree_vendas.heading("Valor Total", text="Valor Total")
        tree_vendas.heading("Forma de Pagamento", text="Forma de Pagamento")
        tree_vendas.pack(fill="both", expand=True)

        # Função para carregar as vendas da data selecionada na tabela
        def carregar_vendas(data_selecionada=None):
            # Limpa a tabela de vendas
            for item in tree_vendas.get_children():
                tree_vendas.delete(item)

            # Se a data não for fornecida, usa a data selecionada no DateEntry
            if not data_selecionada:
                data_selecionada = data_entry.get_date()

            # Seleciona as vendas realizadas na data selecionada
            sql_vendas_dia = "SELECT ID, DATA, horario, VALOR_TOTAL, FORMA_PAGAMENTO FROM TBL_VENDAS WHERE DATA = :1"
            self.cursor.execute(sql_vendas_dia, (data_selecionada,))
            vendas = self.cursor.fetchall()

            # Variáveis para calcular os totais por forma de pagamento
            total_dinheiro = 0
            total_pix = 0
            total_credito = 0
            total_debito = 0
            total_geral = 0

            # Preenche a tabela com as vendas da data selecionada e calcula os totais
            for venda in vendas:
                id_venda, data, horario, valor_total, forma_pagamento = venda

                # Formata a data para exibir apenas a data, sem hora
                data_formatada = data.strftime("%Y-%m-%d")
                tree_vendas.insert("", "end", values=(id_venda, data_formatada, horario, valor_total, forma_pagamento))

                total_geral += valor_total

                if "dinheiro" in forma_pagamento:
                    total_dinheiro += valor_total
                elif "pix" in forma_pagamento:
                    total_pix += valor_total
                elif "credito" in forma_pagamento:
                    total_credito += valor_total
                elif "debito" in forma_pagamento:
                    total_debito += valor_total

            # Exibe os totais na tela
            label_totais.configure(text=f"Total em Dinheiro: R$ {total_dinheiro:.2f}\n"
                                        f"Total em PIX: R$ {total_pix:.2f}\n"
                                        f"Total em Crédito: R$ {total_credito:.2f}\n"
                                        f"Total em Débito: R$ {total_debito:.2f}\n"
                                        f"Total Geral: R$ {total_geral:.2f}")

        # Label para exibir os totais
        label_totais = ctk.CTkLabel(janela_caixa, text="")
        label_totais.pack(pady=10)

        # Botão para carregar as vendas da data selecionada
        botao_carregar = ctk.CTkButton(janela_caixa, text="Carregar Vendas da Data", command=carregar_vendas)
        botao_carregar.pack(pady=10)

        # Carregar vendas do dia atual ao abrir a janela
        data_atual = datetime.now().date()
        carregar_vendas(data_atual)


    def confirm_exit(self):
        """
        Exibe uma mensagem de confirmação ao sair do programa.
        """
        if messagebox.askokcancel("Sair", "Você tem certeza que deseja sair?"):
            self.connection.close()
            self.root.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    MainScreen(root)
