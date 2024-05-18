import tkinter as tk
from tkinter import messagebox
import oracledb
import customtkinter as ctk
import fc

class CalculadoraPrecoVenda:
    def __init__(self, root, entry_preco_venda_principal):
        self.root = root
        self.root.title("Calculadora de Preço de Venda")
        self.entry_preco_venda_principal = entry_preco_venda_principal
        self.connection = fc.conectar_banco()
        self.cursor = self.connection.cursor()
        self.tela_calculo_venda()

    def calcular_preco_venda(self):
        try:
            ca = float(self.entry_custo_produto.get())
            iv = float(self.entry_custo_imposto.get())
            cf = float(self.entry_percentual_custo_fixo.get())
            co = float(self.entry_percentual_custo_operacional.get())
            ml = float(self.margem_lucro_var.get())
            cv = float(self.entry_comissao_venda.get())
            preco_venda = ca / (1 - ((iv + cf + co + ml + cv) / 100))
            self.atualizar_preco_venda(preco_venda)
        except ValueError:
            self.atualizar_preco_venda("Erro")

    def atualizar_preco_venda(self, preco):
        self.entry_preco_venda.configure(state="normal")
        self.entry_preco_venda.delete(0, tk.END)
        self.entry_preco_venda.insert(0, "{:.2f}".format(preco) if isinstance(preco, float) else preco)
        self.entry_preco_venda.configure(state="readonly")

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

    def criar_campos_entrada(self, frame):
        label_rendimento_mensal = ctk.CTkLabel(frame, text="Rendimento bruto Mensal:")
        label_rendimento_mensal.grid(row=0, column=0, sticky=tk.W, pady=2, padx=2)
        self.entry_rendimento_mensal = ctk.CTkEntry(frame, width=100)
        self.entry_rendimento_mensal.grid(row=0, column=1, sticky=tk.W, pady=2, padx=2)

        label_custo_fixo = ctk.CTkLabel(frame, text="Custo Fixo:")
        label_custo_fixo.grid(row=1, column=0, sticky=tk.W, pady=2, padx=2)
        self.entry_custo_fixo = ctk.CTkEntry(frame, width=100)
        self.entry_custo_fixo.grid(row=1, column=1, sticky=tk.W, pady=2, padx=2)

        label_custo_mercadoria = ctk.CTkLabel(frame, text="Custo total das Mercadorias:")
        label_custo_mercadoria.grid(row=0, column=4, sticky=tk.W, pady=2, padx=2)
        self.entry_custo_mercadoria = ctk.CTkEntry(frame, width=100)
        self.entry_custo_mercadoria.grid(row=0, column=5, sticky=tk.W, pady=2, padx=2)

        label_custo_operacional = ctk.CTkLabel(frame, text="Custo operacional:")
        label_custo_operacional.grid(row=1, column=4, sticky=tk.W, pady=2, padx=2)
        self.entry_custo_operacional = ctk.CTkEntry(frame, width=100)
        self.entry_custo_operacional.grid(row=1, column=5, sticky=tk.W, pady=2, padx=2)

        label_percentual_custo_fixo = ctk.CTkLabel(frame, text="Percentual do Custo Fixo:")
        label_percentual_custo_fixo.grid(row=5, column=0, sticky=tk.W, pady=1, padx=2)
        self.entry_percentual_custo_fixo = ctk.CTkEntry(frame, width=100, state="readonly")
        self.entry_percentual_custo_fixo.grid(row=5, column=1, sticky=tk.W, pady=1, padx=2)

        label_percentual_custo_operacional = ctk.CTkLabel(frame, text="Percentual do Custo Operacional:")
        label_percentual_custo_operacional.grid(row=6, column=0, sticky=tk.W, pady=1, padx=2)
        self.entry_percentual_custo_operacional = ctk.CTkEntry(frame, width=100, state="readonly")
        self.entry_percentual_custo_operacional.grid(row=6, column=1, sticky=tk.W, pady=1, padx=2)

        label_custo_imposto = ctk.CTkLabel(frame, text="Percentual do imposto:")
        label_custo_imposto.grid(row=7, column=0, sticky=tk.W, pady=1, padx=2)
        self.entry_custo_imposto = ctk.CTkEntry(frame, width=100)
        self.entry_custo_imposto.grid(row=7, column=1, sticky=tk.W, pady=1, padx=2)

        label_custo_produto = ctk.CTkLabel(frame, text="Custo do Produto:")
        label_custo_produto.grid(row=8, column=0, sticky=tk.W, pady=1, padx=2)
        self.entry_custo_produto = ctk.CTkEntry(frame, width=100)
        self.entry_custo_produto.grid(row=8, column=1, sticky=tk.W, pady=1, padx=2)

        label_comissao_venda = ctk.CTkLabel(frame, text="Percentual da Comissão Venda:")
        label_comissao_venda.grid(row=9, column=0, sticky=tk.W, pady=2, padx=2)
        self.entry_comissao_venda = ctk.CTkEntry(frame, width=100)
        self.entry_comissao_venda.grid(row=9, column=1, sticky=tk.W, pady=2, padx=2)

        label_margem_lucro = ctk.CTkLabel(frame, text="Percentual da Margem de Lucro:")
        label_margem_lucro.grid(row=10, column=0, sticky=tk.W, pady=3, padx=2)
        self.margem_lucro_var = tk.StringVar()
        self.margem_lucro_var.trace("w", lambda name, index, mode, sv=self.margem_lucro_var: self.atualizar_status_margem_lucro())
        self.entry_margem_lucro = ctk.CTkEntry(frame, width=100, textvariable=self.margem_lucro_var)
        self.entry_margem_lucro.grid(row=10, column=1, sticky=tk.W, pady=3, padx=2)
        
        self.label_margem_lucro_status = ctk.CTkLabel(frame, text="...")
        self.label_margem_lucro_status.grid(row=10, column=2, sticky=tk.W, pady=3, padx=2)

        label_preco_venda = ctk.CTkLabel(frame, text="Preço de Venda:")
        label_preco_venda.grid(row=11, column=0, sticky=tk.W, pady=3, padx=2)
        self.entry_preco_venda = ctk.CTkEntry(frame, width=100, state="readonly")
        self.entry_preco_venda.grid(row=11, column=1, sticky=tk.W, pady=3, padx=2)

    def criar_botoes(self, frame):
        btn_calcular_percentuais = ctk.CTkButton(frame, text="Calcular Percentuais", command=lambda: fc.calcular_custos_e_percentuais(
            self.entry_rendimento_mensal, self.entry_custo_fixo, self.entry_custo_mercadoria, 
            self.entry_custo_operacional, self.entry_percentual_custo_fixo, self.entry_percentual_custo_operacional))
        btn_calcular_percentuais.grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)

        btn_calcular_preco_venda = ctk.CTkButton(frame, text="Calcular Preço de Venda", command=self.calcular_preco_venda)
        btn_calcular_preco_venda.grid(row=12, column=0, sticky=tk.W, pady=5, padx=5)

        btn_voltar = ctk.CTkButton(frame, text="Salvar", command=self.salvar)
        btn_voltar.grid(row=12, column=1, sticky=tk.W, pady=5, padx=5)

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
        preco_venda = self.entry_preco_venda.get()
        self.entry_preco_venda_principal.configure(state="normal")
        self.entry_preco_venda_principal.delete(0, tk.END)
        self.entry_preco_venda_principal.insert(0, preco_venda)
        self.entry_preco_venda_principal.configure(state="readonly")
        self.nova_janela.destroy()
        self.root.deiconify()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = CalculadoraPrecoVenda(root)
    root.mainloop()
