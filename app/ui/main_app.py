import tkinter as tk
from tkinter import messagebox

from app.config import APP_TITLE, MAIN_MIN_HEIGHT, MAIN_MIN_WIDTH, MAIN_SIZE, TOPICS
from app.ui.topic_window import VentanaTema


class AplicacionPrincipal:
    """Ventana principal de la aplicación - Explorador de Temas.
    
    Controla la interfaz principal, maneja el menú, los botones de temas,
    el contador del dashboard y el cierre de la aplicación.
    
    Coordina la apertura de ventanas secundarias (VentanaTema) y hace seguimiento
    del estado de cierre de cada una mediante callbacks.
    
    Atributos:
        root (tk.Tk): Ventana principal de Tkinter.
        topic_windows (dict): Diccionario de ventanas abiertas por tema.
        opened_topics (set): Conjunto de temas que han sido abiertos en algún momento.
        active_topic_name (str): Nombre del tema actualmente activo (mostrado en el dashboard).
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(MAIN_SIZE)
        self.root.minsize(MAIN_MIN_WIDTH, MAIN_MIN_HEIGHT)
        self.root.resizable(True, True)
        self.root.configure(bg="#E9F1F4")
        self._centrar_ventana()

        self.topic_windows = {}
        self.opened_topics = set()
        self.active_topic_name = None

        self._construir_menu()
        self._construir_ui()
        self._actualizar_estado_boton_cerrar()

    def _centrar_ventana(self):
        """Centra la ventana principal en el centro de la pantalla.
        
        Se llama al iniciar la aplicación y también desde el menú 
        para permitir al usuario recentrar la ventana si es necesario.
        """
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _construir_menu(self):
        """Construye los menús desplegables de la interfaz.
        
        Crea dos menús:
        - Archivo: con opciones para recentrar y cerrar la aplicación.
        - Ayuda: muestra la información del equipo (Grupo 7, integrantes).
        """
        menu_principal = tk.Menu(self.root)
        self.root.config(menu=menu_principal)

        menu_archivo = tk.Menu(menu_principal, tearoff=0)
        menu_principal.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Recentrar ventana", command=self._centrar_ventana)
        menu_archivo.add_separator()
        menu_archivo.add_command(
            label="Cerrar ventana principal", command=self.solicitar_cierre
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

    def _construir_ui(self):
        """Construye la interfaz de usuario de la ventana principal.
        
        Crea:
        - Título y subtítulo
        - Etiquetas del contador/dashboard
        - Botones para abrir cada tema
        - Botón rojo para cerrar la aplicación
        """
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
                command=lambda t=topic: self.abrir_ventana_tema(t),
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
            command=self.solicitar_cierre,
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

    def abrir_ventana_tema(self, topic_name: str):
        """Abre una ventana secundaria para un tema específico.
        
        Si el tema ya está abierto, trae esa ventana al frente en lugar
        de crear una nueva. Si es la primera vez, crea la VentanaTema
        y registra los callbacks para actualizaciones del contador y cierre.
        
        Args:
            topic_name (str): Nombre del tema a abrir (clave en TOPICS).
        """
        if topic_name in self.topic_windows and self.topic_windows[topic_name].esta_viva():
            self.topic_windows[topic_name].enfocar()
            self.active_topic_name = topic_name
            return

        self.root.update_idletasks()

        # El dashboard se actualiza con cada ventana nueva abierta.
        topic_window = VentanaTema(
            self.root,
            topic_name,
            TOPICS[topic_name],
            on_countdown_update=self.actualizar_contador_principal,
            on_window_closed=self.al_cerrar_tema,
        )
        self.topic_windows[topic_name] = topic_window
        self.opened_topics.add(topic_name)
        self.active_topic_name = topic_name
        self._actualizar_estado_boton_cerrar()

    def actualizar_contador_principal(self, topic_name: str, seconds_left: int, unlocked: bool):
        """Actualiza el contador del dashboard cuando una ventana cambia su estado.
        
        Solo actualiza si topic_name es la ventana actualmente activa
        (la última abierta). Muestra los segundos restantes o 0s cuando se desbloquea.
        
        Args:
            topic_name (str): Nombre del tema que envió la actualización.
            seconds_left (int): Segundos restantes en el contador.
            unlocked (bool): True si el cierre ya está desbloqueado (seconds_left <= 0).
        """
        if topic_name != self.active_topic_name:
            return

        if unlocked:
            self.main_countdown_label.configure(text="0s")
            return

        self.main_countdown_label.configure(text=f"{seconds_left}s")

    def al_cerrar_tema(self, topic_name: str):
        """Maneja el evento de cierre de una ventana secundaria.
        
        Cuando se cierra una ventana secundaria (VentanaTema):
        1. Si era la ventana activa, cambia a otra abierta si existe.
        2. Limpia el contador del dashboard si no quedan ventanas.
        3. Actualiza el estado del botón de cierre de 10s en espera.
        
        Args:
            topic_name (str): Nombre del tema que se cerró.
        """
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

    def _hay_ventanas_bloqueadas(self) -> bool:
        """Verifica si hay alguna ventana secundaria aún dentro de su contador de 10 segundos.
        
        Itera sobre todas las ventanas abiertas y revisa si:
        1. La ventana existe (esta_viva()).
        2. Aún no ha pasado el cierre desbloqueado (cierre_desbloqueado() == False).
        
        Retorna:
            bool: True si hay al menos una ventana bloqueada, False si todas están desbloqueadas.
        """
        for topic_window in self.topic_windows.values():
            if topic_window.esta_viva() and not topic_window.cierre_desbloqueado():
                return True
        return False

    def _actualizar_estado_boton_cerrar(self):
        """Actualiza el estado (habilitado/deshabilitado) del botón de cierre.
        
        El botón rojo se mantiene DESHABILITADO mientras hay ventanas secundarias
        dentro de su período de bloqueo de 10 segundos. Una vez que todas están
        desbloqueadas, el botón se habilita.
        
        Este método se ejecuta cada 300ms para verificar en tiempo real el estado
        de los contadores.
        """
        if self._hay_ventanas_bloqueadas():
            self.close_main_button.configure(state=tk.DISABLED)
        else:
            self.close_main_button.configure(state=tk.NORMAL)

        # Se repite para reflejar el avance de los contadores en tiempo real.
        self.root.after(300, self._actualizar_estado_boton_cerrar)

    def solicitar_cierre(self):
        """Solicita confirmación del usuario antes de cerrar la aplicación.
        
        Antes de permitir el cierre:
        1. Verifica que todas las ventanas secundarias hayan pasado sus 10 segundos.
        2. Si hay ventanas aún bloqueadas, muestra un mensaje de espera.
        3. Si todo está desbloqueado, muestra un cuadro de confirmación.
        4. Si el usuario confirma, destruye la aplicación.
        """
        if self._hay_ventanas_bloqueadas():
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

    def ejecutar(self):
        """Inicia el loop de eventos de Tkinter para mostrar la ventana principal."""
        self.root.mainloop()
