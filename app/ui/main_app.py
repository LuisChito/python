import tkinter as tk
from tkinter import messagebox

from app.config import APP_TITLE, MAIN_MIN_HEIGHT, MAIN_MIN_WIDTH, MAIN_SIZE, TOPICS
from app.ui.topic_window import TopicWindow


class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(MAIN_SIZE)
        self.root.minsize(MAIN_MIN_WIDTH, MAIN_MIN_HEIGHT)
        self.root.resizable(True, True)
        self.root.configure(bg="#E9F1F4")
        self._center_window()

        self.topic_windows = {}
        self.opened_topics = set()
        self.active_topic_name = None

        self._build_menu()
        self._build_ui()
        self._refresh_main_close_button_state()

    def _center_window(self):
        """Centra la ventana principal en pantalla al arrancar la app."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _build_menu(self):
        """Crea menus desplegables para acciones rapidas de la interfaz."""
        menu_principal = tk.Menu(self.root)
        self.root.config(menu=menu_principal)

        menu_archivo = tk.Menu(menu_principal, tearoff=0)
        menu_principal.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Recentrar ventana", command=self._center_window)
        menu_archivo.add_separator()
        menu_archivo.add_command(
            label="Cerrar ventana principal", command=self.request_main_close
        )

        menu_ayuda = tk.Menu(menu_principal, tearoff=0)
        menu_principal.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(
            label="Equipo",
            command=lambda: messagebox.showinfo(
                "Integrantes",
                "Equipo 7\nCarrillo\nRuiz\nSalazar",
                parent=self.root,
            ),
        )

    def _build_ui(self):
        title = tk.Label(
            self.root,
            text="Explorador de Temas",
            font=("Segoe UI", 30, "bold"),
            fg="#12344D",
            bg="#E9F1F4",
        )
        title.pack(pady=(28, 10))

        subtitle = tk.Label(
            self.root,
            text="Selecciona un tema para abrir su ventana secundaria.",
            font=("Segoe UI", 13),
            fg="#1F4E63",
            bg="#E9F1F4",
        )
        subtitle.pack(pady=(0, 24))

        self.main_countdown_hint_label = tk.Label(
            self.root,
            text="Espera a que termine el contador para habilitar el cierre.",
            font=("Segoe UI", 10),
            fg="#6B7280",
            bg="#E9F1F4",
        )
        self.main_countdown_hint_label.pack(pady=(0, 2))

        self.main_countdown_label = tk.Label(
            self.root,
            text="",
            font=("Segoe UI", 11, "bold"),
            fg="#8A5A00",
            bg="#E9F1F4",
        )
        self.main_countdown_label.pack(pady=(0, 12))

        buttons_frame = tk.Frame(self.root, bg="#E9F1F4")
        buttons_frame.pack(pady=10)

        for topic in TOPICS:
            btn = tk.Button(
                buttons_frame,
                text=topic,
                command=lambda t=topic: self.open_topic_window(t),
                font=("Segoe UI", 12, "bold"),
                bg="#2F6F88",
                fg="white",
                activebackground="#3F89A6",
                activeforeground="white",
                bd=0,
                padx=18,
                pady=12,
                cursor="hand2",
            )
            btn.pack(side="left", padx=8)

        self.close_main_button = tk.Button(
            self.root,
            text="Cerrar ventana principal",
            command=self.request_main_close,
            font=("Segoe UI", 11, "bold"),
            bg="#C44536",
            fg="white",
            activebackground="#A3362A",
            activeforeground="white",
            bd=0,
            padx=16,
            pady=10,
            cursor="hand2",
        )
        self.close_main_button.pack(pady=(18, 20))

    def open_topic_window(self, topic_name: str):
        if topic_name in self.topic_windows and self.topic_windows[topic_name].is_alive():
            self.topic_windows[topic_name].focus()
            self.active_topic_name = topic_name
            return

        self.root.update_idletasks()

        # El dashboard se actualiza con cada ventana nueva abierta.
        topic_window = TopicWindow(
            self.root,
            topic_name,
            TOPICS[topic_name],
            on_countdown_update=self.update_main_countdown,
            on_window_closed=self.on_topic_closed,
        )
        self.topic_windows[topic_name] = topic_window
        self.opened_topics.add(topic_name)
        self.active_topic_name = topic_name
        self._refresh_main_close_button_state()

    def update_main_countdown(self, topic_name: str, seconds_left: int, unlocked: bool):
        """Actualiza el contador del dashboard solo si es la ventana activa (última abierta)."""
        if topic_name != self.active_topic_name:
            return

        if unlocked:
            self.main_countdown_label.configure(text="0s")
            return

        self.main_countdown_label.configure(text=f"{seconds_left}s")

    def on_topic_closed(self, topic_name: str):
        if self.active_topic_name == topic_name:
            # Si se cierra la ventana activa, cambiar a otra abierta si existe.
            self.active_topic_name = None
            for other_topic, window in self.topic_windows.items():
                if window.is_alive():
                    self.active_topic_name = other_topic
                    break
            # Limpiar el label si no hay más ventanas activas.
            if self.active_topic_name is None:
                self.main_countdown_label.configure(text="")
        self._refresh_main_close_button_state()

    def _has_locked_open_windows(self) -> bool:
        """True si hay secundarias abiertas cuyo contador aun no termina."""
        for topic_window in self.topic_windows.values():
            if topic_window.is_alive() and not topic_window.is_close_unlocked():
                return True
        return False

    def _refresh_main_close_button_state(self):
        """Habilita o bloquea el boton rojo segun el estado de secundarias."""
        if self._has_locked_open_windows():
            self.close_main_button.configure(state=tk.DISABLED)
        else:
            self.close_main_button.configure(state=tk.NORMAL)

        # Se repite para reflejar el avance de los contadores en tiempo real.
        self.root.after(300, self._refresh_main_close_button_state)

    def request_main_close(self):
        if self._has_locked_open_windows():
            messagebox.showinfo(
                "Cierre bloqueado",
                "Debes esperar a que pasen los 10 segundos de las ventanas abiertas.",
                parent=self.root,
            )
            return

        if len(self.opened_topics) == len(TOPICS):
            mensaje = (
                "Ya abriste todas las ventanas secundarias.\n\n"
                "Deseas cerrar la ventana principal?"
            )
        else:
            mensaje = "Deseas cerrar el programa y todas sus ventanas?"

        confirm = messagebox.askyesno(
            "Confirmar cierre",
            mensaje,
            parent=self.root,
        )
        if confirm:
            self.root.destroy()

    def run(self):
        self.root.mainloop()
