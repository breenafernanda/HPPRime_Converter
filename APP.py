import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from funcionalidades import pdf_to_hp_prime, display_pdf
import fitz

def select_pdf():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if pdf_path:
        pdf_label.config(text=pdf_path)
        root.pdf_path = pdf_path
        root.current_page = 0
        root.total_pages = fitz.open(pdf_path).page_count
        update_page()

def process_files():
    if hasattr(root, 'pdf_path'):
        pdf_to_hp_prime(root.pdf_path)
    else:
        messagebox.showwarning("Atenção", "Por favor, selecione o arquivo PDF.")

def update_page():
    display_pdf(root.pdf_path, pdf_display, root.current_page)
    page_label.config(text=f"{root.current_page + 1} / {root.total_pages}")

def prev_page(event=None):
    if root.current_page > 0:
        root.current_page -= 1
        update_page()

def next_page(event=None):
    if root.current_page < root.total_pages - 1:
        root.current_page += 1
        update_page()

def on_enter(e):
    e.widget['background'] = '#444444'

def on_leave(e):
    e.widget['background'] = '#333333'

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = 40  # Para iniciar no topo da tela
    root.geometry(f'{width}x{height}+{x}+{y}')

root = tk.Tk()
root.title("Converter PDF para HP Prime")
root.resizable(False, False)
root.configure(bg='#2e2e2e')
center_window(root, 1024, 680)

style = ttk.Style()
style.theme_use('clam')

# Estilo para botões
style.configure("TButton",
                font=("Helvetica", 12),
                padding=10,
                background='#444444',
                foreground='white',
                borderwidth=0,
                focusthickness=3,
                focuscolor='none')

# Estilo para labels
style.configure("TLabel",
                background='#2e2e2e',
                foreground='white')

# Frame principal
main_frame = tk.Frame(root, bg='#2e2e2e')
main_frame.pack(fill=tk.BOTH, expand=True)

# Frame esquerdo para os botões
left_frame = tk.Frame(main_frame, bg='#2e2e2e')
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

# Centralizar verticalmente os widgets
left_inner_frame = tk.Frame(left_frame, bg='#2e2e2e')
left_inner_frame.pack(expand=True)

pdf_label = ttk.Label(left_inner_frame, text="Nenhum arquivo PDF selecionado")
pdf_label.pack(pady=5)

pdf_button = ttk.Button(left_inner_frame, text="Selecionar PDF", command=select_pdf)
pdf_button.pack(pady=5)
pdf_button.bind("<Enter>", on_enter)
pdf_button.bind("<Leave>", on_leave)

process_button = ttk.Button(left_inner_frame, text="Converter PDF", command=process_files)
process_button.pack(pady=20)
process_button.bind("<Enter>", on_enter)
process_button.bind("<Leave>", on_leave)

# Frame direito para o visualizador de PDF
right_frame = tk.Frame(main_frame, bg='#2e2e2e')
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

pdf_display = tk.Label(right_frame, bg='#2e2e2e')
pdf_display.pack(padx=10, pady=10)

# Paginador
paginator_frame = tk.Frame(right_frame, bg='#2e2e2e')
paginator_frame.pack(pady=10)

prev_button = tk.Button(paginator_frame, text="←", command=prev_page, font=("Helvetica", 16), width=5, height=1, bg='#444444', fg='white')
prev_button.pack(side=tk.LEFT)
prev_button.bind("<Enter>", on_enter)
prev_button.bind("<Leave>", on_leave)

page_label = ttk.Label(paginator_frame, text="0 / 0")
page_label.pack(side=tk.LEFT, padx=10)

next_button = tk.Button(paginator_frame, text="→", command=next_page, font=("Helvetica", 16), width=5, height=1, bg='#444444', fg='white')
next_button.pack(side=tk.LEFT)
next_button.bind("<Enter>", on_enter)
next_button.bind("<Leave>", on_leave)

# Rodapé de doação
footer_frame = tk.Frame(root, bg='#2e2e2e')
footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

donation_label = tk.Label(footer_frame, text="☕ Se esse software te ajudou de alguma forma, sinta-se livre para me pagar um cafezinho, caso queira, é claro!\n$  PIX: CNPJ 51.510.521/0001-20", bg='#2e2e2e', fg='white', font=("Helvetica", 12))
donation_label.pack(pady=10)

root.current_page = 0
root.total_pages = 0

# Vincular as setas do teclado às funções de paginação
root.bind('<Left>', prev_page)
root.bind('<Right>', next_page)

root.mainloop()
