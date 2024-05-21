import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import fc


class CalculadoraPrecoVenda:
    def __init__(self, root, entry_preco_venda_principal, cadastro_produto):

        self.root = root
        self.root.title("Calculadora de Preço de Venda")
        self.entry_preco_venda_principal = entry_preco_venda_principal
        self.connection = fc.conectar_banco()
        self.cursor = self.connection.cursor()
        self.cadastro_produto = cadastro_produto
        self.tela_calculo_venda()
        self.preencher_campos_composicao()
    def calcular_preco_venda(self):
        # Limpar mensagem de erro antes de calcular
        self.label_composicao_preco.configure(text="")

        try:
            ca = float(self.entry_custo_produto.get())
            iv = float(self.entry_custo_imposto.get())
            cf = float(self.entry_percentual_custo_fixo.get())
            co = float(self.entry_percentual_custo_operacional.get())
            ml = float(self.margem_lucro_var.get())
            cv = float(self.entry_comissao_venda.get())
            
            total_percentage = iv + cf + co + ml + cv

            if total_percentage >= 100:
                raise ValueError("A soma das porcentagens não pode ser maior ou igual a 100%")

            preco_venda = ca / (1 - (total_percentage / 100))

            composicao = {
                "Custo do Produto": ca,
                "Imposto": iv * preco_venda / 100,
                "Custo Fixo": cf * preco_venda / 100,
                "Custo Operacional": co * preco_venda / 100,
                "Margem de Lucro": ml * preco_venda / 100,
                "Comissão de Venda": cv * preco_venda / 100,
            }

            self.atualizar_preco_venda(preco_venda)
            self.atualizar_descricao(preco_venda, composicao)
        except ValueError as e:
            self.atualizar_preco_venda("Erro")
            self.label_composicao_preco.configure(text=f"Erro ao calcular a composição do preço: {str(e)}")

    def preencher_campos_composicao(self):
        if (self.codigo_de_barra != 0):
            query = """
                SELECT percentual_custo_fixo, percentual_custo_operacional, percentual_imposto, 
                    percentual_comissao_venda, percentual_margem_lucro 
                FROM tbl_produto_composicao 
                WHERE codigo_de_barras = :codigo_de_barras
            """
            self.cursor.execute(query, {"codigo_de_barras": self.codigo_de_barras})
            result = self.cursor.fetchone()

            if result:
                self.entry_percentual_custo_fixo.configure(state="normal")
                self.entry_percentual_custo_operacional.configure(state="normal")
                self.entry_custo_imposto.configure(state="normal")
                self.entry_comissao_venda.configure(state="normal")
                self.entry_margem_lucro.configure(state="normal")

                self.entry_percentual_custo_fixo.delete(0, tk.END)
                self.entry_percentual_custo_operacional.delete(0, tk.END)
                self.entry_custo_imposto.delete(0, tk.END)
                self.entry_comissao_venda.delete(0, tk.END)
                self.entry_margem_lucro.delete(0, tk.END)

                self.entry_percentual_custo_fixo.insert(0, str(result[0]))
                self.entry_percentual_custo_operacional.insert(0, str(result[1]))
                self.entry_custo_imposto.insert(0, str(result[2]))
                self.entry_comissao_venda.insert(0, str(result[3]))
                self.entry_margem_lucro.insert(0, str(result[4]))

                self.entry_percentual_custo_fixo.configure(state="readonly")
                self.entry_percentual_custo_operacional.configure(state="readonly")
                self.entry_custo_imposto.configure(state="readonly")
                self.entry_comissao_venda.configure(state="readonly")
                self.entry_margem_lucro.configure(state="readonly")

    def atualizar_preco_venda(self, preco):
        self.entry_preco_venda.configure(state="normal")
        self.entry_preco_venda.delete(0, tk.END)
        self.entry_preco_venda.insert(0, "{:.2f}".format(preco) if isinstance(preco, float) else preco)
        self.entry_preco_venda.configure(state="readonly")

    def atualizar_descricao(self, preco_venda, composicao):
            self.label_val_preco_venda.configure(text=f"R$ {preco_venda:.2f}")
            for chave, valor in composicao.items():
                percentual = (valor / preco_venda) * 100
                if chave == "Custo do Produto":
                    self.label_val_custo_aquisicao.configure(text=f"R$ {valor:.2f}")
                    self.label_perc_custo_aquisicao.configure(text=f"{percentual:.2f}%")
                elif chave == "Imposto":
                    self.label_val_impostos.configure(text=f"R$ {valor:.2f}")
                    self.label_perc_impostos.configure(text=f"{percentual:.2f}%")
                elif chave == "Custo Fixo":
                    self.label_val_custo_fixo.configure(text=f"R$ {valor:.2f}")
                    self.label_perc_custo_fixo.configure(text=f"{percentual:.2f}%")
                elif chave == "Custo Operacional":
                    self.label_val_custo_operacional.configure(text=f"R$ {valor:.2f}")
                    self.label_perc_custo_operacional.configure(text=f"{percentual:.2f}%")
                elif chave == "Margem de Lucro":
                    self.label_val_margem_lucro.configure(text=f"R$ {valor:.2f}")
                    self.label_perc_margem_lucro.configure(text=f"{percentual:.2f}%")
                elif chave == "Comissão de Venda":
                    self.label_val_comissao_venda.configure(text=f"R$ {valor:.2f}")
                    self.label_perc_comissao_venda.configure(text=f"{percentual:.2f}%")

    def tela_calculo_venda(self):
        self.root.iconify()
        self.nova_janela = ctk.CTkToplevel(self.root)
        self.nova_janela.title("Calculadora de Preço de Venda")
        self.nova_janela.resizable(False, False)
        self.nova_janela.protocol("WM_DELETE_WINDOW", self.fechar_janela_calculo)
        frame = ctk.CTkFrame(self.nova_janela)
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.criar_campos_entrada(frame)
        self.criar_botoes(frame)
        self.descricao(frame)

    def criar_campos_entrada(self, frame):
        # Frame para a primeira seção
        frame_secao1 = ctk.CTkFrame(frame)
        frame_secao1.grid(row=0, column=0, columnspan=6, sticky=tk.W, padx=2, pady=2)

        # Rendimento bruto Mensal
        label_rendimento_mensal = ctk.CTkLabel(frame_secao1, text="Rendimento bruto Mensal:")
        label_rendimento_mensal.grid(row=0, column=0, sticky=tk.W, pady=2, padx=2)
        self.entry_rendimento_mensal = ctk.CTkEntry(frame_secao1, width=100)
        self.entry_rendimento_mensal.grid(row=0, column=1, sticky=tk.W, pady=2, padx=2)

        # Custo Fixo
        label_custo_fixo = ctk.CTkLabel(frame_secao1, text="Custo Fixo:")
        label_custo_fixo.grid(row=1, column=0, sticky=tk.W, pady=2, padx=2)
        self.entry_custo_fixo = ctk.CTkEntry(frame_secao1, width=100)
        self.entry_custo_fixo.grid(row=1, column=1, sticky=tk.W, pady=2, padx=2)

        # Custo total das Mercadorias
        label_custo_mercadoria = ctk.CTkLabel(frame_secao1, text="Custo total das Mercadorias:")
        label_custo_mercadoria.grid(row=0, column=4, sticky=tk.W, pady=2, padx=2)
        self.entry_custo_mercadoria = ctk.CTkEntry(frame_secao1, width=100)
        self.entry_custo_mercadoria.grid(row=0, column=5, sticky=tk.W, pady=2, padx=2)

        # Custo Operacional
        label_custo_operacional = ctk.CTkLabel(frame_secao1, text="Custo Operacional:")
        label_custo_operacional.grid(row=1, column=4, sticky=tk.W, pady=2, padx=2)
        self.entry_custo_operacional = ctk.CTkEntry(frame_secao1, width=100)
        self.entry_custo_operacional.grid(row=1, column=5, sticky=tk.W, pady=2, padx=2)

        btn_calcular_percentuais = ctk.CTkButton(frame_secao1, text="Calcular Percentuais", command=lambda: fc.calcular_custos_e_percentuais(
            self.entry_rendimento_mensal, self.entry_custo_fixo, self.entry_custo_mercadoria,
            self.entry_custo_operacional, self.entry_percentual_custo_fixo, self.entry_percentual_custo_operacional))
        btn_calcular_percentuais.grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)

   
        # Percentual do Custo Fixo
        label_percentual_custo_fixo = ctk.CTkLabel(frame_secao1, text="Percentual do Custo Fixo:")
        label_percentual_custo_fixo.grid(row=3, column=0, sticky=tk.W, pady=2, padx=2)
        self.entry_percentual_custo_fixo = ctk.CTkEntry(frame_secao1, width=100, state="readonly")
        self.entry_percentual_custo_fixo.grid(row=3, column=1, sticky=tk.W, pady=2, padx=2)

        # Percentual do Custo Operacional
        label_percentual_custo_operacional = ctk.CTkLabel(frame_secao1, text="Percentual do Custo Operacional:")
        label_percentual_custo_operacional.grid(row=4, column=0, sticky=tk.W, pady=2, padx=2)
        self.entry_percentual_custo_operacional = ctk.CTkEntry(frame_secao1, width=100, state="readonly")
        self.entry_percentual_custo_operacional.grid(row=4, column=1, sticky=tk.W, pady=2, padx=2)

        # Percentual do Imposto
        label_custo_imposto = ctk.CTkLabel(frame_secao1, text="Percentual do Imposto:")
        label_custo_imposto.grid(row=5, column=0, sticky=tk.W, pady=2, padx=2)
        self.entry_custo_imposto = ctk.CTkEntry(frame_secao1, width=100)
        self.entry_custo_imposto.grid(row=5, column=1, sticky=tk.W, pady=2, padx=2)

        # Custo do Produto
        label_custo_produto = ctk.CTkLabel(frame_secao1, text="Custo do Produto:")
        label_custo_produto.grid(row=6, column=0, sticky=tk.W, pady=2, padx=2)
        self.entry_custo_produto = ctk.CTkEntry(frame_secao1, width=100)
        self.entry_custo_produto.grid(row=6, column=1, sticky=tk.W, pady=2, padx=2)

        # Percentual da Comissão de Venda
        label_comissao_venda = ctk.CTkLabel(frame_secao1, text="Percentual da Comissão de Venda:")
        label_comissao_venda.grid(row=7, column=0, sticky=tk.W, pady=2, padx=2)
        self.entry_comissao_venda = ctk.CTkEntry(frame_secao1, width=100)
        self.entry_comissao_venda.grid(row=7, column=1, sticky=tk.W, pady=2, padx=2)

        # Percentual da Margem de Lucro
        label_margem_lucro = ctk.CTkLabel(frame_secao1, text="Percentual da Margem de Lucro:")
        label_margem_lucro.grid(row=8, column=0, sticky=tk.W, pady=2, padx=2)
        self.margem_lucro_var = tk.StringVar()
        self.margem_lucro_var.trace("w", lambda name, index, mode, sv=self.margem_lucro_var: self.atualizar_status_margem_lucro())
        self.entry_margem_lucro = ctk.CTkEntry(frame_secao1, width=100, textvariable=self.margem_lucro_var)
        self.entry_margem_lucro.grid(row=8, column=1, sticky=tk.W, pady=2, padx=2)

        self.label_margem_lucro_status = ctk.CTkLabel(frame_secao1, text="   ")
        self.label_margem_lucro_status.grid(row=8, column=2, sticky=tk.W, pady=2, padx=2)

        # Preço de Venda
        label_preco_venda = ctk.CTkLabel(frame_secao1, text="Preço de Venda:")
        label_preco_venda.grid(row=9, column=0, sticky=tk.W, pady=2, padx=2)
        self.entry_preco_venda = ctk.CTkEntry(frame_secao1, width=100, state="readonly")
        self.entry_preco_venda.grid(row=9, column=1, sticky=tk.W, pady=2, padx=2)

        # Composição do Preço ( para mostrar mensagem de erro)
        self.label_composicao_preco = ctk.CTkLabel(frame, text="")
        self.label_composicao_preco.grid(row=9, column=0, columnspan=6, sticky=tk.W, pady=5, padx=2)



    def criar_botoes(self, frame):

        btn_calcular_preco_venda = ctk.CTkButton(frame, text="Calcular Preço de Venda", command=self.calcular_preco_venda)
        btn_calcular_preco_venda.grid(row=4, column=1, sticky=tk.W, pady=5, padx=5)

        btn_voltar = ctk.CTkButton(frame, text="Salvar", command=self.salvar)
        btn_voltar.grid(row=4, column=0, sticky=tk.W, pady=5, padx=5)

    def atualizar_status_margem_lucro(self):
        try:
            margem_lucro = float(self.margem_lucro_var.get())
            if margem_lucro >= 0 and margem_lucro <= 15:
                self.label_margem_lucro_status.configure(text="Baixo", text_color="red")
            elif margem_lucro > 15 and margem_lucro <= 30:
                self.label_margem_lucro_status.configure(text="Moderado", text_color="orange")
            elif margem_lucro > 30 and margem_lucro <= 45:
                self.label_margem_lucro_status.configure(text="Alto", text_color="green")
            elif margem_lucro > 45:
                self.label_margem_lucro_status.configure(text="Muito Alto", text_color="blue")
        except ValueError:
            self.label_margem_lucro_status.configure(text="Inválido", text_color="black")

    def fechar_janela_calculo(self):
        self.nova_janela.destroy()
        self.root.deiconify()

    def salvar(self):
        # Salva o preço de venda
        preco_venda = self.entry_preco_venda.get()
        self.entry_preco_venda_principal.configure(state="normal")
        self.entry_preco_venda_principal.delete(0, tk.END)
        self.entry_preco_venda_principal.insert(0, preco_venda)
        self.entry_preco_venda_principal.configure(state="readonly")
        
        # Atualiza os percentuais na instância de CadastrarProduto ou editar_produto
        self.cadastro_produto.percentual_custo_fixo = float(self.entry_percentual_custo_fixo.get())
        self.cadastro_produto.percentual_custo_operacional = float(self.entry_percentual_custo_operacional.get())
        self.cadastro_produto.percentual_imposto = float(self.entry_custo_imposto.get())
        self.cadastro_produto.percentual_comissao_venda = float(self.entry_comissao_venda.get())
        self.cadastro_produto.percentual_margem_lucro = float(self.margem_lucro_var.get())
        
        self.nova_janela.destroy()
        self.root.deiconify()


    def descricao(self, frame):
        # Configuração do frame de descrição dos itens
        self.descricao_frame = ctk.CTkFrame(frame)
        self.descricao_frame.grid(row=0, column=6, columnspan=2, rowspan=10, sticky="ns", padx=2, pady=2)
        self.descricao_frame.grid_columnconfigure(0, weight=1)
        self.descricao_frame.grid_columnconfigure(1, weight=1)
        self.descricao_frame.grid_columnconfigure(2, weight=1)

        # Labels para os cabeçalhos das descrições
        label_header_descricao = ctk.CTkLabel(self.descricao_frame, text="Descrição")
        label_header_descricao.grid(row=0, column=0)

        label_desc_preco_venda = ctk.CTkLabel(self.descricao_frame, text="A.Preço de Venda")
        label_desc_preco_venda.grid(row=1, column=0)

        label_desc_custo_aquisicao = ctk.CTkLabel(self.descricao_frame, text="B.Custo de Aquisição")
        label_desc_custo_aquisicao.grid(row=2, column=0)

        label_desc_custo_operacional = ctk.CTkLabel(self.descricao_frame, text="C.Custo Operacional")
        label_desc_custo_operacional.grid(row=3, column=0)

        label_desc_custo_fixo = ctk.CTkLabel(self.descricao_frame, text="D.Custo Fixo")
        label_desc_custo_fixo.grid(row=4, column=0)

        label_desc_impostos = ctk.CTkLabel(self.descricao_frame, text="E.Impostos")
        label_desc_impostos.grid(row=5, column=0)

        label_desc_margem_lucro = ctk.CTkLabel(self.descricao_frame, text="F.Margem de Lucro")
        label_desc_margem_lucro.grid(row=6, column=0)

        label_desc_comissao_venda = ctk.CTkLabel(self.descricao_frame, text="G.Comissão de Venda")
        label_desc_comissao_venda.grid(row=7, column=0)

        # Subframe para valores e percentuais
        self.descricao_subframe = ctk.CTkFrame(self.descricao_frame)
        self.descricao_subframe.grid(row=0, rowspan=8, column=2, sticky="ew")
        self.descricao_subframe.grid_columnconfigure(0, weight=1)
        self.descricao_subframe.grid_columnconfigure(1, weight=1)

        # Labels para valores
        label_header_valor = ctk.CTkLabel(self.descricao_subframe, text="Valor")
        label_header_valor.grid(row=0, column=0, padx=16, pady=3)

        self.label_val_preco_venda = ctk.CTkLabel(self.descricao_subframe, text="R$ 0.00")
        self.label_val_preco_venda.grid(row=1, column=0, padx=16, pady=3)

        self.label_val_custo_aquisicao = ctk.CTkLabel(self.descricao_subframe, text="R$ 0.00")
        self.label_val_custo_aquisicao.grid(row=2, column=0, padx=16, pady=3)

        self.label_val_custo_operacional = ctk.CTkLabel(self.descricao_subframe, text="R$ 0.00")
        self.label_val_custo_operacional.grid(row=3, column=0, padx=16, pady=3)

        self.label_val_custo_fixo = ctk.CTkLabel(self.descricao_subframe, text="R$ 0.00")
        self.label_val_custo_fixo.grid(row=4, column=0, padx=16, pady=3)

        self.label_val_impostos = ctk.CTkLabel(self.descricao_subframe, text="R$ 0.00")
        self.label_val_impostos.grid(row=5, column=0, padx=16, pady=3)

        self.label_val_margem_lucro = ctk.CTkLabel(self.descricao_subframe, text="R$ 0.00")
        self.label_val_margem_lucro.grid(row=6, column=0, padx=16, pady=3)

        self.label_val_comissao_venda = ctk.CTkLabel(self.descricao_subframe, text="R$ 0.00")
        self.label_val_comissao_venda.grid(row=7, column=0, padx=16, pady=3)

        # Labels para percentuais
        label_header_percentual = ctk.CTkLabel(self.descricao_subframe, text="%")
        label_header_percentual.grid(row=0, column=1, padx=16, pady=3)

        self.label_perc_preco_venda = ctk.CTkLabel(self.descricao_subframe, text="0.00%")
        self.label_perc_preco_venda.grid(row=1, column=1, padx=16, pady=3)

        self.label_perc_custo_aquisicao = ctk.CTkLabel(self.descricao_subframe, text="0.00%")
        self.label_perc_custo_aquisicao.grid(row=2, column=1, padx=16, pady=3)

        self.label_perc_custo_operacional = ctk.CTkLabel(self.descricao_subframe, text="0.00%")
        self.label_perc_custo_operacional.grid(row=3, column=1, padx=16, pady=3)

        self.label_perc_custo_fixo = ctk.CTkLabel(self.descricao_subframe, text="0.00%")
        self.label_perc_custo_fixo.grid(row=4, column=1, padx=16, pady=3)

        self.label_perc_impostos = ctk.CTkLabel(self.descricao_subframe, text="0.00%")
        self.label_perc_impostos.grid(row=5, column=1, padx=16, pady=3)

        self.label_perc_margem_lucro = ctk.CTkLabel(self.descricao_subframe, text="0.00%")
        self.label_perc_margem_lucro.grid(row=6, column=1, padx=16, pady=3)

        self.label_perc_comissao_venda = ctk.CTkLabel(self.descricao_subframe, text="0.00%")
        self.label_perc_comissao_venda.grid(row=7, column=1, padx=16, pady=3)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    entry_preco_venda_principal = ctk.CTkEntry(root)
    app = CalculadoraPrecoVenda(root, entry_preco_venda_principal)
    root.mainloop()
