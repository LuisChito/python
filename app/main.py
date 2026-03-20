from tkinter import messagebox

from app.config import validar_imagenes
from app.ui.main_app import AplicacionPrincipal


def main():
    """Punto de entrada de la aplicación.
    
    Realiza validación de imágenes necesarias y luego inicia la interfaz gráfica.
    """
    faltantes = validar_imagenes()
    if faltantes:
        mensaje = "No se encontraron estas imagenes requeridas:\n\n"
        mensaje += "\n".join(faltantes)
        messagebox.showerror("Imagenes faltantes", mensaje)
        return

    app = AplicacionPrincipal()
    app.ejecutar()
