from pathlib import Path
import tkinter as tk
from tkinter import messagebox

from app.config import (
    CHILD_MIN_HEIGHT,
    CHILD_MIN_WIDTH,
    CHILD_SIZE_FACTOR,
    CLOSE_DELAY_SECONDS,
)


class VentanaTema:
    """Ventana secundaria que muestra una imagen de un tema.
    
    La ventana implementa un contador de 10 segundos (CLOSE_DELAY_SECONDS) que bloquea
    el cierre durante ese tiempo. Después de los 10 segundos, el usuario puede cerrar
    la ventana normalmente. Mientras está contando, notifica a la ventana principal
    del progreso del countdown.
    
    Atributos:
        topic_name (str): Nombre del tema que se mostrará en la ventana.
        image_path (Path): Ruta al archivo PNG de la imagen del tema.
        allow_close (bool): Indica si la ventana puede ser cerrada (después de 10s).
        seconds_left (int): Segundos restantes del contador al cierre.
        on_countdown_update (callable): Callback para notificar cambios en el contador.
        on_window_closed (callable): Callback para notificar cuando se cierra la ventana.
    """
    def __init__(
        self,
        parent: tk.Tk,
        topic_name: str,
        image_path: Path,
        on_countdown_update=None,
        on_window_closed=None,
    ):
        self.topic_name = topic_name
        self.image_path = image_path
        self.allow_close = False
        self.seconds_left = CLOSE_DELAY_SECONDS
        self.on_countdown_update = on_countdown_update
        self.on_window_closed = on_window_closed

        self.window = tk.Toplevel(parent)
        self.window.title(topic_name)

        # Se calcula un tamano menor al de la principal para no taparla completamente.
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()

        win_w = max(CHILD_MIN_WIDTH, int(parent_w * CHILD_SIZE_FACTOR))
        win_h = max(CHILD_MIN_HEIGHT, int(parent_h * CHILD_SIZE_FACTOR))

        # Todas las secundarias se abren centradas en la pantalla.
        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()
        win_x = (screen_w - win_w) // 2
        win_y = (screen_h - win_h) // 2
        self.window.geometry(f"{win_w}x{win_h}+{win_x}+{win_y}")
        self.window.minsize(CHILD_MIN_WIDTH, CHILD_MIN_HEIGHT)
        self.window.resizable(True, True)

        self.window.protocol("WM_DELETE_WINDOW", self._al_cerrar_ventana)

        self.bg_label = tk.Label(self.window, bd=0)
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        panel = tk.Frame(self.window, bg="#0B2E4A")
        panel.pack(side="bottom", fill="x", padx=12, pady=12)

        self.info_label = tk.Label(
            panel,
            text="Puedes mover y redimensionar esta ventana.",
            font=("Segoe UI", 11, "bold"),
            bg="#0B2E4A",
            fg="white",
            pady=8,
        )
        self.info_label.pack(fill="x")

        self.countdown_label = tk.Label(
            panel,
            text=f"Boton de cierre disponible en: {self.seconds_left}s",
            font=("Segoe UI", 10),
            bg="#0B2E4A",
            fg="#FFD166",
        )
        self.countdown_label.pack(pady=(0, 8))

        self.close_button = tk.Button(
            panel,
            text="Cerrar esta ventana",
            command=self._cerrar_con_boton,
            font=("Segoe UI", 10, "bold"),
            bg="#F0B429",
            fg="#102A43",
            activebackground="#FFD166",
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
        )
        self.close_button.pack_forget()

        self.photo = None
        self._cargar_fondo()
        self._contar_regresivo()

    def _cargar_fondo(self):
        """Carga la imagen PNG del tema como fondo de la ventana.
        
        Si el archivo no existe o no puede ser leído como PNG, muestra
        un mensaje de error centrado en la ventana en su lugar.
        """
        if not self.image_path.exists():
            self.bg_label.configure(
                text=f"No se encontro la imagen para: {self.topic_name}",
                bg="#183A4A",
                fg="white",
                font=("Segoe UI", 12, "bold"),
            )
            return

        try:
            self.photo = tk.PhotoImage(file=str(self.image_path))
            self.bg_label.configure(image=self.photo)
        except tk.TclError:
            self.bg_label.configure(
                text="No se pudo cargar la imagen PNG.",
                bg="#183A4A",
                fg="white",
                font=("Segoe UI", 12, "bold"),
            )

    def _habilitar_boton_cerrar(self):
        """Habilita el cierre de la ventana después de que el contador llega a 0.
        
        Establece allow_close=True, muestra el botón de cierre, actualiza los
        mensajes de la ventana y notifica a la ventana principal que se puede cerrar.
        """
        self.allow_close = True
        self.close_button.pack(pady=(0, 8))
        self.info_label.configure(text="Ya puedes cerrar esta ventana con el boton.")
        self.countdown_label.configure(text="Ya puedes cerrar esta ventana.", fg="#9BE564")
        if self.on_countdown_update:
            self.on_countdown_update(self.topic_name, 0, True)

    def _contar_regresivo(self):
        """Ejecuta el contador regresivo de 10 segundos (CLOSE_DELAY_SECONDS).
        
        Se ejecuta recursivamente cada 1 segundo, actualizando el label
        y notificando al callback on_countdown_update. Cuando llega a 0,
        llama a _habilitar_boton_cerrar().
        """
        if self.seconds_left <= 0:
            self._habilitar_boton_cerrar()
            return

        self.countdown_label.configure(
            text=f"Boton de cierre disponible en: {self.seconds_left}s"
        )
        if self.on_countdown_update:
            self.on_countdown_update(self.topic_name, self.seconds_left, False)
        self.seconds_left -= 1
        self.window.after(1000, self._contar_regresivo)

    def _al_cerrar_ventana(self):
        """Maneja el evento del botón X (cerrar ventana del sistema).
        
        Si el contador ya terminó (allow_close=True), permite cerrar.
        Si no, muestra un mensaje informado al usuario que debe esperar
        los 10 segundos o usar el botón de cierre.
        """
        if self.allow_close:
            self.window.destroy()
            return

        messagebox.showinfo(
            "Cierre bloqueado",
            "Solo puedes cerrar esta ventana con su boton (despues de 10 segundos).",
            parent=self.window,
        )

    def _cerrar_con_boton(self):
        """Cierra la ventana y notifica al callback on_window_closed.
        
        Este método es llamado cuando el usuario hace clic en el botón
        de cierre de la ventana secundaria (después de los 10 segundos).
        """
        self.window.destroy()
        if self.on_window_closed:
            self.on_window_closed(self.topic_name)

    def cerrar_desde_principal(self):
        """Permite cerrar esta ventana desde la ventana principal.
        
        Se llama cuando el usuario cierra el programa completo,
        una vez que todas las ventanas ya pasó el bloqueo de 10 segundos.
        """
        self._cerrar_con_boton()

    def cierre_desbloqueado(self) -> bool:
        """Indica si el cierre de esta ventana ya está desbloqueado (contador en 0).
        
        Retorna:
            bool: True si ya pasaron los 10 segundos, False si aún está contando.
        """
        return self.seconds_left <= 0

    def enfocar(self):
        """Trae la ventana al frente y le da el foco de entrada."""
        self.window.deiconify()
        self.window.lift()
        self.window.focus_force()

    def esta_viva(self) -> bool:
        """Verifica si la ventana aún existe y no ha sido destruida.
        
        Retorna:
            bool: True si la ventana existe, False si fue cerrada.
        """
        return bool(self.window.winfo_exists())
