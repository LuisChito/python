import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Ventanas secundarias abiertas para habilitar cierre al final
ventanas_abiertas = 0

def centrar_ventana(ventana):
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

def abrir_ventana_secundaria(tema):
    global ventanas_abiertas
    ventana_secundaria = tk.Toplevel(ventana_principal)
    ventana_secundaria.title(tema)
    
    ventana_secundaria.protocol("WM_DELETE_WINDOW", lambda: None)  # Ignorar el evento de cierre
    
    ventana_secundaria.configure(bg="#f0f0f0")
    
    try:
        imagen = Image.open(BASE_DIR / "imgs" / f"{tema}.png")
        
        nuevo_ancho = 600
        nuevo_alto = 400
        imagen_redimensionada = imagen.resize((nuevo_ancho, nuevo_alto))
        
        imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)
        
        fondo = tk.Label(ventana_secundaria, image=imagen_tk, bg="#f0f0f0")
        # Guardar referencia evita que tkinter libere la imagen
        fondo.image = imagen_tk
        fondo.pack(fill=tk.BOTH, expand=True)
    except FileNotFoundError:
        fondo = tk.Label(ventana_secundaria, text=f"Imagen no encontrada para {tema}", bg="#f0f0f0", fg="black")
        fondo.pack(fill=tk.BOTH, expand=True)
    
    centrar_ventana(ventana_secundaria)
    
    def mostrar_boton_cerrar():
        time.sleep(10)
        boton_cerrar = tk.Button(ventana_secundaria, text="Cerrar", command=ventana_secundaria.destroy, bg="#ff6666", fg="white")
        boton_cerrar.pack(pady=10)
    
    # Mostrar el botón de cerrar después de 10 segundos
    ventana_secundaria.after(10000, mostrar_boton_cerrar)
    
    ventanas_abiertas += 1
    
    if ventanas_abiertas == 3:
        boton_cerrar_principal.config(state=tk.NORMAL)

def confirmar_cierre():
    if messagebox.askyesno("Cerrar", "¿Estás seguro de que quieres cerrar la ventana principal?"):
        ventana_principal.destroy()

ventana_principal = tk.Tk()
ventana_principal.title("7SB_Equipo_6")

ventana_principal.protocol("WM_DELETE_WINDOW", lambda: None)

ventana_principal.geometry("600x800")

ventana_principal.configure(bg="#e0e0e0")

centrar_ventana(ventana_principal)

menu_principal = tk.Menu(ventana_principal)
ventana_principal.config(menu=menu_principal)

menu_archivo = tk.Menu(menu_principal, tearoff=0)
menu_principal.add_cascade(label="Archivo", menu=menu_archivo)
menu_archivo.add_command(label="Salir", command=confirmar_cierre)

frame_contenedor = tk.Frame(ventana_principal, bg="#e0e0e0")
frame_contenedor.pack(expand=True, fill=tk.BOTH)

titulo = tk.Label(
    frame_contenedor,
    text="Configurador de Sistemas Expertos",
    font=("Arial", 24, "bold"),
    bg="#e0e0e0",
    fg="#333333"
)
titulo.pack(pady=20)

frame_botones = tk.Frame(frame_contenedor, bg="#e0e0e0")
frame_botones.pack(expand=True)

boton_autobus = tk.Button(
    frame_botones,
    text="Base de Conocimientos",
    command=lambda: abrir_ventana_secundaria("base_de_conocimientos"),
    width=20,
    height=3,
    font=("Arial", 14),
    bg="#4CAF50",
    fg="white"
)
boton_autobus.pack(pady=10)

boton_tren = tk.Button(
    frame_botones,
    text="Motor de Inferencia",
    command=lambda: abrir_ventana_secundaria("motor_de_inferencia"),
    width=20,
    height=3,
    font=("Arial", 14),
    bg="#2196F3",
    fg="white"
)
boton_tren.pack(pady=10)

boton_taxi = tk.Button(
    frame_botones,
    text="Interfaz de Usuario",
    command=lambda: abrir_ventana_secundaria("interfaz_de_usuario"),
    width=20,
    height=3,
    font=("Arial", 14),
    bg="#FF9800",
    fg="white"
)
boton_taxi.pack(pady=10)

# Se activa cuando se abren las 3 ventanas secundarias
boton_cerrar_principal = tk.Button(
    frame_botones,
    text="Cerrar Ventana Principal",
    command=confirmar_cierre,
    width=20,
    height=2,
    font=("Arial", 12),
    bg="#f44336",
    fg="white",
    state=tk.DISABLED
)
boton_cerrar_principal.pack(pady=10)

ventana_principal.mainloop()