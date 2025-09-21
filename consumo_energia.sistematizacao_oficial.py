''' Aplicação que apresenta que calcula o Consumo diário de uma residência
composta por 06 cômodos, sendo 01 sala, 02 quartos, 01 cozinha, 01 banheiro e
área de serviço. '''

#Autor(a): Mariana Rabelo de Farias - 2º semestre de ADS - @UniCEUB


# Importação das bbliotecas
import tkinter as tk
from tkinter import messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
import tempfile

# Criação da classe Consumo de Energia
class AppConsumoEnergia:
    def __init__(self, root):
        self.root = root
        self.root.title("Consumo de Energia - Futurista")
        self.root.geometry("1100x650")
        self.root.configure(bg="#f4f6f8")

        # Variáveis de dados de entrada e saída
        self.consumos_dados = {}
        self.relatorio_texto = ""
        self.fig_grafico = None

        # Criar menu
        self.criar_menu()

        # Criar frames
        self.criar_frame_inputs()
        self.criar_frame_resultado()
        self.criar_frame_grafico()

    # Estrruturação do Menu
    def criar_menu(self):
        menu_bar = tk.Menu(self.root)

        arquivo_menu = tk.Menu(menu_bar, tearoff=0)
        arquivo_menu.add_command(label="Gerar Excel", command=self.gerar_excel)
        arquivo_menu.add_command(label="Gerar PDF", command=self.gerar_pdf)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label="Sair", command=self.root.destroy)
        menu_bar.add_cascade(label="Arquivo", menu=arquivo_menu)

        ajuda_menu = tk.Menu(menu_bar, tearoff=0)
        ajuda_menu.add_command(label="Sobre", command=self.mostrar_sobre)
        menu_bar.add_cascade(label="Ajuda", menu=ajuda_menu)

        self.root.config(menu=menu_bar)

    #  Frames da Aplicação 
    def criar_frame_inputs(self):
        self.frame_inputs = tk.Frame(self.root, bg="#f0f0f0", padx=15, pady=15, relief="raised", bd=2)
        self.frame_inputs.pack(side="left", fill="y", padx=10, pady=10)

        labels = ["Quarto 1 (kWh):", "Quarto 2 (kWh):", "Banheiro (kWh):",
                  "Cozinha (kWh):", "Sala (kWh):", "Área de Serviço (kWh):", "Valor da Tarifa (R$/kWh):"]
        self.entries = []

        for i, text in enumerate(labels):
            tk.Label(self.frame_inputs, text=text, font=("Segoe UI", 11), bg="#f0f0f0").grid(row=i, column=0, sticky="e", pady=5)
            entry = tk.Entry(self.frame_inputs, font=("Segoe UI", 11), bg="white", fg="#333", relief="flat")
            entry.grid(row=i, column=1, pady=5)
            self.entries.append(entry)

        # Botões com características futuristas - Experiência do Usuário
        self.criar_botoes_futuristas()

    # Criação da classe Resultados
    def criar_frame_resultado(self):
        self.frame_resultado = tk.Frame(self.root, bg="#e8f4f8", relief="raised", bd=2, padx=10, pady=10)
        self.frame_resultado.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        self.txt_resultado = tk.Text(self.frame_resultado, wrap="word", state="disabled", font=("Segoe UI", 11),
                                     height=15, bg="white", fg="#333")
        self.txt_resultado.pack(fill="both", expand=True)

    # Criação do frame para o gráfico de consumo 
    def criar_frame_grafico(self):
        self.frame_grafico = tk.Frame(self.root, bg="#e8f4f8", relief="raised", bd=2, padx=10, pady=10)
        self.frame_grafico.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

    #  Botões futuristas 
    def criar_botoes_futuristas(self):
        btn_calcular = self.criar_botao_futurista("Calcular Consumo", self.calcular_consumo, "#2ecc71")
        btn_calcular.grid(row=7, column=0, columnspan=2, sticky="we", pady=5)

        btn_excel = self.criar_botao_futurista("Gerar Excel", self.gerar_excel, "#3498db")
        btn_excel.grid(row=8, column=0, columnspan=2, sticky="we", pady=5)

        btn_pdf = self.criar_botao_futurista("Gerar PDF", self.gerar_pdf, "#9b59b6")
        btn_pdf.grid(row=9, column=0, columnspan=2, sticky="we", pady=5)

        btn_fechar = self.criar_botao_futurista("Fechar Aplicação", self.root.destroy, "#e74c3c")
        btn_fechar.grid(row=10, column=0, columnspan=2, sticky="we", pady=5)

    def criar_botao_futurista(self, text, command, cor_base="#1abc9c"):
        btn = tk.Button(self.frame_inputs, text=text, command=command,
                        bg=cor_base, fg="white", font=("Segoe UI", 11, "bold"),
                        relief="flat", bd=0, padx=12, pady=6, activebackground="#16a085", activeforeground="white")
        def on_enter(e):
            btn['bg'] = "#16a085"
        def on_leave(e):
            btn['bg'] = cor_base
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    #  Funcionalidades 
    def calcular_consumo(self):
        try:
            valores = [float(entry.get()) for entry in self.entries]
            quarto1, quarto2, banheiro, cozinha, sala, area_servico, tarifa = valores

            consumo_total = sum(valores[:-1])
            val_quarto1 = quarto1 * tarifa
            val_quarto2 = quarto2 * tarifa
            val_banheiro = banheiro * tarifa
            val_cozinha = cozinha * tarifa
            val_sala = sala * tarifa
            val_area = area_servico * tarifa
            valor_total = consumo_total * tarifa

            self.relatorio_texto = (
                f"--- Relatório de Consumo Diário ---\n\n"
                f"Quarto 1: {quarto1:.2f} kWh -> R$ {val_quarto1:.2f}\n"
                f"Quarto 2: {quarto2:.2f} kWh -> R$ {val_quarto2:.2f}\n"
                f"Banheiro: {banheiro:.2f} kWh -> R$ {val_banheiro:.2f}\n"
                f"Cozinha: {cozinha:.2f} kWh -> R$ {val_cozinha:.2f}\n"
                f"Sala: {sala:.2f} kWh -> R$ {val_sala:.2f}\n"
                f"Área de Serviço: {area_servico:.2f} kWh -> R$ {val_area:.2f}\n\n"
                f"Consumo total diário: {consumo_total:.2f} kWh -> R$ {valor_total:.2f}\n"
                f"Consumo mensal estimado (30 dias): {consumo_total*30:.2f} kWh -> R$ {valor_total*30:.2f}\n\n"
                f"💡 Valores baseados em uma família com 4 pessoas (2 adultos, 1 adolescente e 1 criança)"
            )

            self.consumos_dados = {
                "Cômodo": ["Quarto 1", "Quarto 2", "Banheiro", "Cozinha", "Sala", "Área de Serviço"],
                "Consumo (kWh)": [quarto1, quarto2, banheiro, cozinha, sala, area_servico],
                "Valor (R$)": [val_quarto1, val_quarto2, val_banheiro, val_cozinha, val_sala, val_area]
            }

            # Atualizar Text
            self.txt_resultado.config(state="normal")
            self.txt_resultado.delete(1.0, tk.END)
            self.txt_resultado.insert(tk.END, self.relatorio_texto)
            self.txt_resultado.config(state="disabled")

            # Criar gráfico
            self.criar_grafico()

        except ValueError:
            messagebox.showerror("Erro", "Preencha todos os campos com valores numéricos.")

    def criar_grafico(self):
        labels = self.consumos_dados["Cômodo"]
        consumos = self.consumos_dados["Consumo (kWh)"]

        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        self.fig_grafico, ax = plt.subplots(figsize=(4.5, 4.5))
        ax.pie(consumos, labels=labels, autopct=lambda p: '{:.1f}%'.format(p),
               startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6'])
        ax.set_title("Participação no Consumo Diário", fontsize=12)
        canvas_fig = FigureCanvasTkAgg(self.fig_grafico, master=self.frame_grafico)
        canvas_fig.draw()
        canvas_fig.get_tk_widget().pack(fill="both", expand=True)

    def gerar_excel(self):
        if not self.consumos_dados:
            messagebox.showwarning("Aviso", "Calcule o consumo antes de gerar o relatório.")
            return
        df = pd.DataFrame(self.consumos_dados)
        caminho = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if caminho:
            df.to_excel(caminho, index=False)
            messagebox.showinfo("Sucesso", f"Relatório Excel gerado: {caminho}")

    def gerar_pdf(self):
        if not self.consumos_dados:
            messagebox.showwarning("Aviso", "Calcule o consumo antes de gerar o relatório.")
            return
        caminho = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if caminho:
            c = pdf_canvas.Canvas(caminho, pagesize=A4)
            width, height = A4
            y = height - 50
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y, "Relatório de Consumo Diário")
            y -= 30
            c.setFont("Helvetica", 12)
            for i in range(len(self.consumos_dados["Cômodo"])):
                linha = f"{self.consumos_dados['Cômodo'][i]}: {self.consumos_dados['Consumo (kWh)'][i]:.2f} kWh -> R$ {self.consumos_dados['Valor (R$)'][i]:.2f}"
                c.drawString(50, y, linha)
                y -= 20
            y -= 10
            total_consumo = sum(self.consumos_dados["Consumo (kWh)"])
            total_valor = sum(self.consumos_dados["Valor (R$)"])
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, f"Consumo Total: {total_consumo:.2f} kWh")
            y -= 20
            c.drawString(50, y, f"Valor Total: R$ {total_valor:.2f}")
            y -= 30

            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
                self.fig_grafico.savefig(tmpfile.name, bbox_inches='tight')
                c.drawImage(ImageReader(tmpfile.name), 50, y-300, width=500, height=300)
            c.save()
            messagebox.showinfo("Sucesso", f"Relatório PDF gerado: {caminho}")

    def mostrar_sobre(self):
        messagebox.showinfo("Sobre", "Programa de Cálculo de Consumo Diário de Energia\nVersão Futurista Premium\nDesenvolvido em Python com Tkinter")


# Executar aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = AppConsumoEnergia(root)
    root.mainloop()

# EOC