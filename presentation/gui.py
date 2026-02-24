import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from infrastructure.repository import CSVProductRepository
from infrastructure.file_system import LocalFolderCreator
from infrastructure.config_manager import load_config, save_config
from application.use_cases import CreateFolderUseCase


APP_NAME = "StudioFlow – Organizador de Fotos"


class AppController:

    def __init__(self):
        self.config = load_config()
        self.repository = None
        self.folder_creator = LocalFolderCreator()
        self.use_case = None

        if self.config.get("database_path"):
            self.load_repository()

    def load_repository(self):
        try:
            self.repository = CSVProductRepository(
                self.config["database_path"]
            )
            self.use_case = CreateFolderUseCase(
                self.repository,
                self.folder_creator
            )
        except Exception as e:
            messagebox.showerror("Erro ao carregar base", str(e))


def run_app():

    controller = AppController()

    root = tk.Tk()
    root.title(APP_NAME)
    root.geometry("900x600")
    root.minsize(850, 550)

    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(fill="both", expand=True)

    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=0)

    # ==================================================
    # TÍTULO
    # ==================================================

    title_label = ttk.Label(
        main_frame,
        text=APP_NAME,
        font=("Arial", 18, "bold")
    )
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    # ==================================================
    # BASE
    # ==================================================

    ttk.Label(main_frame, text="Base de Dados")\
        .grid(row=1, column=0, sticky="w")

    db_var = tk.StringVar(value=controller.config.get("database_path", ""))

    db_entry = ttk.Entry(main_frame, textvariable=db_var)
    db_entry.grid(row=2, column=0, sticky="ew", pady=5)

    def select_database():
        path = filedialog.askopenfilename(
            filetypes=[("Planilhas", "*.csv *.xlsx")]
        )
        if path:
            db_var.set(path)
            controller.config["database_path"] = path
            save_config(controller.config)
            controller.load_repository()

    ttk.Button(
        main_frame,
        text="Selecionar",
        command=select_database
    ).grid(row=2, column=1, padx=10)

    # ==================================================
    # DESTINO
    # ==================================================

    ttk.Label(main_frame, text="Destino das Pastas")\
        .grid(row=3, column=0, sticky="w", pady=(20, 0))

    dest_var = tk.StringVar(
        value=controller.config.get("destination_path", "")
    )

    dest_entry = ttk.Entry(main_frame, textvariable=dest_var)
    dest_entry.grid(row=4, column=0, sticky="ew", pady=5)

    def select_destination():
        path = filedialog.askdirectory()
        if path:
            dest_var.set(path)
            controller.config["destination_path"] = path
            save_config(controller.config)

    ttk.Button(
        main_frame,
        text="Selecionar",
        command=select_destination
    ).grid(row=4, column=1, padx=10)

    # ==================================================
    # LEITURA DE CÓDIGO
    # ==================================================

    separator = ttk.Separator(main_frame, orient="horizontal")
    separator.grid(row=5, column=0, columnspan=2, sticky="ew", pady=30)

    ttk.Label(
        main_frame,
        text="Leitura do Código de Barra",
        font=("Arial", 14, "bold")
    ).grid(row=6, column=0, columnspan=2, pady=10)

    barcode_entry = ttk.Entry(
        main_frame,
        font=("Arial", 20),
        justify="center"
    )
    barcode_entry.grid(row=7, column=0, columnspan=2,
                       sticky="ew", pady=10)
    barcode_entry.focus()

    # ==================================================
    # RESULTADOS
    # ==================================================

    result_frame = ttk.Frame(main_frame)
    result_frame.grid(row=8, column=0, columnspan=2,
                      sticky="ew", pady=30)

    result_frame.columnconfigure(1, weight=1)

    codigo_produto_var = tk.StringVar()
    familia_var = tk.StringVar()
    cor_var = tk.StringVar()
    pasta_var = tk.StringVar()
    caminho_var = tk.StringVar()

    ttk.Label(result_frame, text="Código Produto:")\
        .grid(row=0, column=0, sticky="w")
    ttk.Label(result_frame, textvariable=codigo_produto_var)\
        .grid(row=0, column=1, sticky="w")

    ttk.Label(result_frame, text="Família:")\
        .grid(row=1, column=0, sticky="w")
    ttk.Label(result_frame, textvariable=familia_var)\
        .grid(row=1, column=1, sticky="w")

    ttk.Label(result_frame, text="Cor:")\
        .grid(row=2, column=0, sticky="w")
    ttk.Label(result_frame, textvariable=cor_var)\
        .grid(row=2, column=1, sticky="w")

    ttk.Label(result_frame, text="Nome da Pasta:")\
        .grid(row=3, column=0, sticky="w")
    ttk.Label(result_frame, textvariable=pasta_var)\
        .grid(row=3, column=1, sticky="w")

    ttk.Label(result_frame, text="Caminho Completo:")\
        .grid(row=4, column=0, sticky="w")
    ttk.Label(result_frame, textvariable=caminho_var)\
        .grid(row=4, column=1, sticky="w")

    status_label = ttk.Label(
        main_frame,
        text="",
        font=("Arial", 12, "bold")
    )
    status_label.grid(row=9, column=0, columnspan=2, pady=10)

    # ==================================================
    # PROCESSAMENTO
    # ==================================================

    def process_barcode(event=None):

        barcode = barcode_entry.get().strip()

        if not controller.use_case:
            messagebox.showerror("Erro", "Selecione a base primeiro.")
            return

        if not dest_var.get():
            messagebox.showerror("Erro", "Selecione pasta destino.")
            return

        try:
            product, folder_name, full_path = controller.use_case.execute(
                barcode,
                dest_var.get()
            )

            codigo_produto_var.set(product.codigo_produto)
            familia_var.set(product.descricao_familia)
            cor_var.set(product.cor)
            pasta_var.set(folder_name)
            caminho_var.set(full_path)

            status_label.config(
                text="✔ Pasta criada com sucesso!",
                foreground="green"
            )

            barcode_entry.delete(0, tk.END)
            barcode_entry.focus()

        except Exception as e:
            status_label.config(
                text=f"Erro: {str(e)}",
                foreground="red"
            )

    barcode_entry.bind("<Return>", process_barcode)

    root.mainloop()