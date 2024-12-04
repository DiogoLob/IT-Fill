import tkinter as tk
from tkinter import filedialog, messagebox, Text
from fpdf import FPDF
from datetime import datetime
import os


class PDFGenerator(FPDF):
    def header(self):
        if app.logo_path:
            self.image(app.logo_path, x=10, y=8, w=30)  # Alinhamento da logo
        self.set_font("Arial", "B", 16)
        self.cell(0, 25, "Instrução de Trabalho Padrão", border=1, align="C", ln=True)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, f"Data de Geração: {datetime.now().strftime('%d/%m/%Y')}", align="R")

    def add_procedure_info(self, procedure_name, tools, epis):
        self.set_font("Arial", size=12)
        self.cell(50, 10, "Procedimento:", border=1)
        self.cell(0, 10, procedure_name, border=1, ln=True)
        self.cell(50, 10, "Ferramentas Utilizadas:", border=1)
        self.cell(0, 10, tools, border=1, ln=True)
        self.cell(50, 10, "EPIs Utilizados:", border=1)
        self.cell(0, 10, epis, border=1, ln=True)
        self.ln(5)

    def add_stage(self, stage_number, stage_title, stage_description, stage_image):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"Etapa {stage_number}: {stage_title}", ln=True, border=1)
        self.ln(5)
        self.set_font("Arial", size=12)
        self.multi_cell(100, 10, stage_description, border=1)  # Descrição
        if stage_image:
            self.image(stage_image, x=120, y=self.get_y() - 120, w=70)  # Imagem à direita
        self.ln(10)


class GeradorInstrucaoTrabalho(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerador de Instrução de Trabalho")
        self.geometry("600x500")
        self.etapas = []
        self.logo_path = None

        # Frame principal
        self.frame_principal = tk.Frame(self)
        self.frame_principal.pack(pady=20)

        tk.Label(self.frame_principal, text="Nome do Procedimento:", font=("Arial", 12)).pack()
        self.nome_procedimento = tk.Entry(self.frame_principal, font=("Arial", 12), width=40)
        self.nome_procedimento.pack(pady=5)

        tk.Label(self.frame_principal, text="Ferramentas Utilizadas:", font=("Arial", 12)).pack()
        self.ferramentas_utilizadas = tk.Entry(self.frame_principal, font=("Arial", 12), width=40)
        self.ferramentas_utilizadas.pack(pady=5)

        tk.Label(self.frame_principal, text="EPIs Utilizados:", font=("Arial", 12)).pack()
        self.epis_utilizados = tk.Entry(self.frame_principal, font=("Arial", 12), width=40)
        self.epis_utilizados.pack(pady=5)

        tk.Button(self.frame_principal, text="Selecionar Logo", command=self.selecionar_logo, bg="#FF9800", fg="white",
                  font=("Arial", 12)).pack(pady=5)

        tk.Button(self.frame_principal, text="Adicionar Etapa", command=self.adicionar_etapa, bg="#4CAF50", fg="white",
                  font=("Arial", 12)).pack(pady=5)

        tk.Button(self.frame_principal, text="Gerar PDF", command=self.gerar_pdf, bg="#2196F3", fg="white",
                  font=("Arial", 12)).pack(pady=10)

        self.lista_etapas = tk.Listbox(self, height=10, font=("Arial", 12))
        self.lista_etapas.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    def selecionar_logo(self):
        """Seleciona a logo da empresa."""
        self.logo_path = filedialog.askopenfilename(title="Selecione a Logo",
                                                    filetypes=[("Arquivos de Imagem", "*.jpg;*.jpeg;*.png;*.bmp")])
        if self.logo_path:
            messagebox.showinfo("Sucesso", "Logo selecionada com sucesso!")

    def adicionar_etapa(self):
        janela_etapa = JanelaEtapa(self)
        self.wait_window(janela_etapa)
        if janela_etapa.etapa:
            self.etapas.append(janela_etapa.etapa)
            self.lista_etapas.insert(tk.END, f"Etapa {len(self.etapas)}: {janela_etapa.etapa['titulo']}")

    def gerar_pdf(self):
        if not self.nome_procedimento.get():
            messagebox.showerror("Erro", "Por favor, insira o nome do procedimento.")
            return
        if not self.etapas:
            messagebox.showerror("Erro", "Por favor, adicione pelo menos uma etapa.")
            return

        pdf = PDFGenerator()
        pdf.add_page()
        pdf.add_procedure_info(
            self.nome_procedimento.get(),
            self.ferramentas_utilizadas.get(),
            self.epis_utilizados.get()
        )

        for idx, etapa in enumerate(self.etapas, 1):
            pdf.add_stage(idx, etapa['titulo'], etapa['descricao'], etapa['imagem'])

        output_path = os.path.join(os.getcwd(), f"{self.nome_procedimento.get()}.pdf")
        pdf.output(output_path)
        messagebox.showinfo("Sucesso", f"PDF '{output_path}' gerado com sucesso!")


class JanelaEtapa(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Adicionar Etapa")
        self.geometry("500x500")
        self.etapa = None

        tk.Label(self, text="Título da Etapa:", font=("Arial", 12)).pack(pady=5)
        self.titulo = tk.Entry(self, font=("Arial", 12), width=40)
        self.titulo.pack(pady=5)

        tk.Label(self, text="Descrição da Etapa:", font=("Arial", 12)).pack(pady=5)
        self.descricao = Text(self, font=("Arial", 12), height=10, width=50)
        self.descricao.pack(pady=5)

        tk.Button(self, text="Carregar Imagem", command=self.carregar_imagem, bg="#FF9800", fg="white",
                  font=("Arial", 12)).pack(pady=5)

        tk.Button(self, text="Salvar Etapa", command=self.salvar_etapa, bg="#4CAF50", fg="white",
                  font=("Arial", 12)).pack(pady=10)
        self.imagem = None

    def carregar_imagem(self):
        caminho_imagem = filedialog.askopenfilename(
            title="Selecione uma imagem", filetypes=[("Arquivos de Imagem", "*.jpg;*.jpeg;*.png;*.bmp")]
        )
        if caminho_imagem:
            self.imagem = caminho_imagem
            messagebox.showinfo("Sucesso", "Imagem carregada com sucesso!")

    def salvar_etapa(self):
        if not self.titulo.get() or not self.descricao.get("1.0", tk.END).strip():
            messagebox.showerror("Erro", "Por favor, preencha todos os campos antes de salvar.")
            return

        self.etapa = {
            "titulo": self.titulo.get(),
            "descricao": self.descricao.get("1.0", tk.END).strip(),
            "imagem": self.imagem
        }
        self.destroy()


if __name__ == "__main__":
    app = GeradorInstrucaoTrabalho()
    app.mainloop()