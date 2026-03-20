from pathlib import Path
import tkinter as tk
from tkinter import messagebox

from app.config import (
    CHILD_MIN_HEIGHT,
    CHILD_MIN_WIDTH,
    CHILD_SIZE_FACTOR,
    CLOSE_DELAY_SECONDS,
)


class TopicWindow:
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

        self.window.protocol("WM_DELETE_WINDOW", self._on_system_close)

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
            command=self._close_with_button,
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
        self._load_background()
        self._tick_countdown()

    def _load_background(self):
        """Carga la imagen del tema; si falla, muestra mensaje."""
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

    def _enable_close_button(self):
        # Al terminar el contador, la ventana queda desbloqueada para cierre.
        self.allow_close = True
        self.close_button.pack(pady=(0, 8))
        self.info_label.configure(text="Ya puedes cerrar esta ventana con el boton.")
        self.countdown_label.configure(text="Ya puedes cerrar esta ventana.", fg="#9BE564")
        if self.on_countdown_update:
            self.on_countdown_update(self.topic_name, 0, True)

    def _tick_countdown(self):
        if self.seconds_left <= 0:
            self._enable_close_button()
            return

        self.countdown_label.configure(
            text=f"Boton de cierre disponible en: {self.seconds_left}s"
        )
        if self.on_countdown_update:
            self.on_countdown_update(self.topic_name, self.seconds_left, False)
        self.seconds_left -= 1
        self.window.after(1000, self._tick_countdown)

    def _on_system_close(self):
        if self.allow_close:
            self.window.destroy()
            return

        messagebox.showinfo(
            "Cierre bloqueado",
            "Solo puedes cerrar esta ventana con su boton (despues de 10 segundos).",
            parent=self.window,
        )

    def _close_with_button(self):
        self.window.destroy()
        if self.on_window_closed:
            self.on_window_closed(self.topic_name)

    def close_from_main(self):
        """Permite cerrar desde el boton de la principal cuando esta desbloqueado."""
        self._close_with_button()

    def is_close_unlocked(self) -> bool:
        return self.seconds_left <= 0

    def focus(self):
        self.window.deiconify()
        self.window.lift()
        self.window.focus_force()

    def is_alive(self) -> bool:
        return bool(self.window.winfo_exists())
