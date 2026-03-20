from tkinter import messagebox

from app.config import validar_imagenes
from app.ui.main_app import MainApp


def main():
    faltantes = validar_imagenes()
    if faltantes:
        mensaje = "No se encontraron estas imagenes requeridas:\n\n"
        mensaje += "\n".join(faltantes)
        messagebox.showerror("Imagenes faltantes", mensaje)
        return

    app = MainApp()
    app.run()
