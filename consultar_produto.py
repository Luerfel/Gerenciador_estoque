import tkinter as tk  
import customtkinter as ctk  
from tkinter import ttk, messagebox  
import oracledb  
import fc
from cp import HillCipher
import numpy as np

class ConsultarProduto():
    def __init__(self, root_parameter):
        self.root = root_parameter
        self.root.title("Consultar Produto")
        self.connection = fc.conectar_banco()
        self.cipher = HillCipher(fc.key_matriz())
        if self.connection:
            self.cursor = self.connection.cursor()
            self.consultar_design()
            self.carregar_produtos()
        else:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            self.root.destroy()
        self.root.mainloop()

    def carregar_produtos(self):
        sql = "SELECT codigo_de_barras, nome, descricao, preco_de_compra, preco_de_venda, fornecedor, unidades FROM tbl_produtos"
        self.cursor.execute(sql)
        produtos = self.cursor.fetchall()
        for produto in produtos:
            codigo, nome, descricao, preco_de_compra, preco_de_venda, fornecedor, unidades = produto

            # Descriptografa o nome e a descrição
            nome = self.cipher.decrypt(nome)
            descricao = self.cipher.decrypt(descricao)
            fornecedor = self.cipher.decrypt(fornecedor)
            self.tree.insert("", "end", values=(codigo, nome, descricao, preco_de_compra, preco_de_venda, fornecedor, unidades))

    def buscar_produto(self):
        termo_busca = self.entry_busca.get()
        tipo_busca = self.combo_tipo_busca.get()
        if tipo_busca == "Código de Barras":
            sql = "SELECT codigo_de_barras, nome, descricao, preco_de_compra, preco_de_venda, fornecedor, unidades FROM tbl_produtos WHERE codigo_de_barras = :TERMOS_BUSCA"
            self.cursor.execute(sql, {"TERMOS_BUSCA": termo_busca})
        else:
            termo_busca = self.cipher.encrypt(termo_busca)
            sql = "SELECT codigo_de_barras, nome, descricao, preco_de_compra, preco_de_venda, fornecedor, unidades FROM tbl_produtos WHERE nome LIKE :TERMOS_BUSCA"
            self.cursor.execute(sql, {"TERMOS_BUSCA": f"%{termo_busca}%"})

        resultados = self.cursor.fetchall()
        if resultados:
            self.tree.delete(*self.tree.get_children())
            for produto in resultados:
                codigo, nome, descricao, preco_de_compra, preco_de_venda, fornecedor, unidades = produto

                # Descriptografa o nome e a descrição
                nome = self.cipher.decrypt(nome)
                descricao = self.cipher.decrypt(descricao)
                fornecedor = self.cipher.decrypt(fornecedor)

                self.tree.insert("", "end", values=(codigo, nome, descricao, preco_de_compra, preco_de_venda, fornecedor, unidades))
        else:
            messagebox.showerror("Erro", "Nenhum resultado encontrado.")

    def consultar_design(self):
        frame = ctk.CTkFrame(self.root)
        frame.pack(fill=ctk.BOTH, expand=True)

        label_titulo = ctk.CTkLabel(frame, text="Consulta de Produtos")
        label_titulo.pack()

        frame_busca = ctk.CTkFrame(frame)
        frame_busca.pack(fill=tk.X)

        label_busca = ctk.CTkLabel(frame_busca, text="Buscar Produto:")
        label_busca.pack(side=tk.LEFT)

        self.entry_busca = ctk.CTkEntry(frame_busca)
        self.entry_busca.pack(side=ctk.LEFT, padx=5, fill=ctk.X, expand=True)

        self.combo_tipo_busca = ttk.Combobox(frame_busca, values=["Código de Barras", "Nome"], state="readonly")
        self.combo_tipo_busca.pack(side=ctk.LEFT)
        self.combo_tipo_busca.current(0)

        button_buscar = ctk.CTkButton(frame_busca, text="Buscar", command=self.buscar_produto)
        button_buscar.pack(side=ctk.LEFT)

        self.tree = ttk.Treeview(frame, columns=("Código de Barras", "Nome", "Descrição", "Preço Compra", "Preço Venda", "Fornecedor", "Unidades"), show="headings")
        self.tree.heading("Código de Barras", text="Código de Barras", anchor="center")
        self.tree.heading("Nome", text="Nome", anchor="center")
        self.tree.heading("Descrição", text="Descrição", anchor="center")
        self.tree.heading("Preço Compra", text="Preço Compra", anchor="center")
        self.tree.heading("Preço Venda", text="Preço Venda", anchor="center")
        self.tree.heading("Fornecedor", text="Fornecedor", anchor="center")
        self.tree.heading("Unidades", text="Unidades", anchor="center")
        self.tree.column("Código de Barras", anchor="center")
        self.tree.column("Nome", anchor="center")
        self.tree.column("Descrição", anchor="center")
        self.tree.column("Preço Compra", anchor="center")
        self.tree.column("Preço Venda", anchor="center")
        self.tree.column("Fornecedor", anchor="center")
        self.tree.column("Unidades", anchor="center")
        self.tree.pack(fill=ctk.BOTH, expand=True)

        self.tree.bind("<Double-1>", self.abrir_janela_produto)

    def abrir_janela_produto(self, event):
        item = self.tree.selection()[0]
        valores = self.tree.item(item, "values")
        codigo = valores[0]

        self.janela_produto = ctk.CTkToplevel(self.root)
        self.janela_produto.title("Detalhes do Produto")

        frame_detalhes = ctk.CTkFrame(self.janela_produto)
        frame_detalhes.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

        sql = """
        SELECT codigo_de_barras, nome, descricao, preco_de_compra, unidades, fornecedor, preco_de_venda
        FROM tbl_produtos
        WHERE codigo_de_barras = :CODIGO_DE_BARRAS
        """
        self.cursor.execute(sql, {"CODIGO_DE_BARRAS": codigo})
        produto = self.cursor.fetchone()
        if produto:
            codigo, nome, descricao, preco_de_compra, unidades, fornecedor, preco_de_venda = produto
            # Descriptografa os campos
            nome = self.cipher.decrypt(nome)
            descricao = self.cipher.decrypt(descricao)
            fornecedor = self.cipher.decrypt(fornecedor)

            label_codigo = ctk.CTkLabel(frame_detalhes, text=f"Código de Barras: {codigo}")
            label_codigo.pack(anchor="w", pady=5)

            label_nome = ctk.CTkLabel(frame_detalhes, text=f"Nome: {nome}")
            label_nome.pack(anchor="w", pady=5)

            label_descricao = ctk.CTkLabel(frame_detalhes, text=f"Descrição: {descricao}")
            label_descricao.pack(anchor="w", pady=5)

            label_unidades = ctk.CTkLabel(frame_detalhes, text=f"Unidades: {unidades}")
            label_unidades.pack(anchor="w", pady=5)

            label_fornecedor = ctk.CTkLabel(frame_detalhes, text=f"Fornecedor: {fornecedor}")
            label_fornecedor.pack(anchor="w", pady=5)

            # Busca a composição do preço
            sql_composicao = """
            SELECT percentual_custo_fixo, percentual_custo_operacional, percentual_imposto, percentual_comissao_venda, percentual_margem_lucro
            FROM tbl_produto_composicao
            WHERE codigo_de_barras = :CODIGO_DE_BARRAS
            """
            self.cursor.execute(sql_composicao, {"CODIGO_DE_BARRAS": codigo})
            composicao = self.cursor.fetchone()
            if composicao:
                percentual_custo_fixo, percentual_custo_operacional, percentual_imposto, percentual_comissao_venda, percentual_margem_lucro = composicao

                # Configuração do frame de descrição dos itens
                descricao_frame = ctk.CTkFrame(frame_detalhes)
                descricao_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

                label_header_descricao = ctk.CTkLabel(descricao_frame, text="Composição do Preço")
                label_header_descricao.grid(row=0, column=0, columnspan=2)

                label_desc_preco_venda = ctk.CTkLabel(descricao_frame, text="A. Preço de Venda")
                label_desc_preco_venda.grid(row=1, column=0)
                label_val_preco_venda = ctk.CTkLabel(descricao_frame, text=f"{preco_de_venda}")
                label_val_preco_venda.grid(row=1, column=1)

                label_desc_custo_aquisicao = ctk.CTkLabel(descricao_frame, text="B. Custo de Aquisição")
                label_desc_custo_aquisicao.grid(row=2, column=0)
                label_val_custo_aquisicao = ctk.CTkLabel(descricao_frame, text=f"{preco_de_compra}")
                label_val_custo_aquisicao.grid(row=2, column=1)

                label_desc_custo_operacional = ctk.CTkLabel(descricao_frame, text="C. Custo Operacional")
                label_desc_custo_operacional.grid(row=3, column=0)
                label_val_custo_operacional = ctk.CTkLabel(descricao_frame, text=f"{percentual_custo_operacional}%")
                label_val_custo_operacional.grid(row=3, column=1)

                label_desc_custo_fixo = ctk.CTkLabel(descricao_frame, text="D. Custo Fixo")
                label_desc_custo_fixo.grid(row=4, column=0)
                label_val_custo_fixo = ctk.CTkLabel(descricao_frame, text=f"{percentual_custo_fixo}%")
                label_val_custo_fixo.grid(row=4, column=1)

                label_desc_impostos = ctk.CTkLabel(descricao_frame, text="E. Impostos")
                label_desc_impostos.grid(row=5, column=0)
                label_val_impostos = ctk.CTkLabel(descricao_frame, text=f"{percentual_imposto}%")
                label_val_impostos.grid(row=5, column=1)

                label_desc_margem_lucro = ctk.CTkLabel(descricao_frame, text="F. Margem de Lucro")
                label_desc_margem_lucro.grid(row=6, column=0)
                label_val_margem_lucro = ctk.CTkLabel(descricao_frame, text=f"{percentual_margem_lucro}%")
                label_val_margem_lucro.grid(row=6, column=1)

                label_desc_comissao_venda = ctk.CTkLabel(descricao_frame, text="G. Comissão de Venda")
                label_desc_comissao_venda.grid(row=7, column=0)
                label_val_comissao_venda = ctk.CTkLabel(descricao_frame, text=f"{percentual_comissao_venda}%")
                label_val_comissao_venda.grid(row=7, column=1)
            else:
                messagebox.showerror("Erro", "Composição do preço não encontrada para este produto.")
        else:
            messagebox.showerror("Erro", "Produto não encontrado.")



# Executa a aplicação
if __name__ == "__main__":
    root = ctk.CTk()  # Cria a janela principal
    ConsultarProduto(root)  # Instancia a classe ConsultarProduto e inicia a aplicação
