# Explorador de Temas - Sistema de Presentación Interactivo

**Equipo 7**: Carrillo, Ruiz, Salazar  
**Curso**: 7º Semestre - Programación en Lógica (Prolog)

---

## 📋 Descripción General

Esta aplicación es un **explorador interactivo de temas** que permite abrir, visualizar y gestionar múltiples ventanas secundarias de forma sincronizada. Cada ventana tiene un **contador de 10 segundos** que bloquea su cierre durante ese período, enseñando al usuario la importancia de los tiempos de espera en sistemas concurrentes.

---

## 🏗️ Estructura del Proyecto

```
ventanas.py                 # Punto de entrada principal
app/                        # Paquete principal de la aplicación
├── main.py               # Inicializador de la app
├── config.py             # Configuración global y constantes
└── ui/                   # Interfaz de usuario
    ├── main_app.py      # Ventana principal (AplicacionPrincipal)
    └── topic_window.py  # Ventanas secundarias (VentanaTema)
imgs/                      # Directorio de imágenes PNG
├── base_de_conocimientos.png
├── motor_de_inferencia.png
└── interfaz_de_usuario.png
```

---

## 🔄 Flujo de Trabajo del Programa

### 1. **INICIO DE LA APLICACIÓN**

```
ventanas.py
    ↓
app.main.main()
    ↓
Validar imágenes (config.validar_imagenes())
    ↓
¿Todas las imágenes existen?
    ├─ NO  → Mostrar error y salir
    └─ SÍ  → Crear AplicacionPrincipal()
```

**Archivo relevante**: `app/main.py`

### 2. **INICIALIZACIÓN DE LA VENTANA PRINCIPAL**

```
AplicacionPrincipal.__init__()
    ├─ Crear tk.Tk() (ventana principal)
    ├─ Configurar tamaño (980x620) y título
    ├─ Centrar en pantalla (_centrar_ventana)
    ├─ Construir menú (_construir_menu)
    │    ├─ "Archivo" → Recentrar, Cerrar
    │    └─ "Ayuda" → Información del Equipo
    ├─ Construir interfaz (_construir_ui)
    │    ├─ Título: "Explorador de Temas"
    │    ├─ Subtítulo informativo
    │    ├─ Área de contador del dashboard (vacío al inicio)
    │    ├─ 3 botones de tema
    │    └─ Botón rojo "Cerrar ventana principal"
    └─ Iniciar actualización de estado del botón
```

**Archivo relevante**: `app/ui/main_app.py`

### 3. **USUARIO HACE CLIC EN UN BOTÓN DE TEMA**

```
Usuario hace clic en "Base de Conocimientos" (o cualquier tema)
    ↓
AplicacionPrincipal.abrir_ventana_tema(tema_name)
    ├─ ¿Ya existe una ventana abierta para este tema?
    │    ├─ SÍ  → Traerla al frente (enfocar()) y retornar
    │    └─ NO  → Crear nueva ventana
    ├─ Crear VentanaTema()
    │    ├─ Nueva ventana Toplevel
    │    ├─ Cargar imagen PNG (_cargar_fondo)
    │    ├─ Crear panel inferior con info y contador
    │    ├─ Inicializar seconds_left = 10
    │    ├─ Registrar callbacks
    │    └─ Iniciar contador regresivo (_contar_regresivo)
    ├─ Guardar en topic_windows{tema_name: ventana}
    ├─ Marcar tema como abierto en opened_topics
    ├─ Establecer como tema activo (active_topic_name)
    └─ Actualizar estado del botón cerrar
```

**Archivos relevantes**: 
- `app/ui/main_app.py` → método `abrir_ventana_tema()`
- `app/ui/topic_window.py` → clase `VentanaTema`

### 4. **EJECUCIÓN DEL CONTADOR REGRESIVO (10→0 segundos)**

```
VentanaTema._contar_regresivo() ← Ejecutada recursivamente cada 1 segundo

├─ ¿seconds_left <= 0?
│    ├─ SÍ  → _habilitar_boton_cerrar()
│    └─ NO  → Continuo...
│
├─ Actualizar label visual: "Botón disponible en: {seconds_left}s"
├─ Notificar al dashboard (callback on_countdown_update)
│    ↓
│    AplicacionPrincipal.actualizar_contador_principal()
│    ├─ ¿Es este tema el actualmente activo?
│    │    ├─ SÍ  → Actualizar label del dashboard
│    │    └─ NO  → Ignorar (el usuario vio otro tema)
│    └─ Mostrar "{seconds_left}s" en el dashboard
│
├─ Decrementar seconds_left--
├─ Programar siguiente ejecución en 1000ms (window.after)
└─ Esperar...
```

**Archivo relevante**: `app/ui/topic_window.py` → método `_contar_regresivo()`

### 5. **CUANDO EL CONTADOR LLEGA A 0**

```
VentanaTema._contar_regresivo() detecta seconds_left <= 0
    ↓
    VentanaTema._habilitar_boton_cerrar()
    ├─ Establecer allow_close = True
    ├─ Mostrar botón de cierre (pack)
    ├─ Cambiar mensaje: "Ya puedes cerrar esta ventana"
    ├─ Cambiar color a verde (#9BE564)
    └─ Notificar dashboard: unlocked=True
         ↓
         AplicacionPrincipal.actualizar_contador_principal()
         └─ Mostrar "0s" en el dashboard
```

**Archivo relevante**: `app/ui/topic_window.py` → método `_habilitar_boton_cerrar()`

### 6. **ACTUALIZACIÓN DEL ESTADO DEL BOTÓN ROJO (Cada 300ms)**

```
AplicacionPrincipal._actualizar_estado_boton_cerrar() 
    ↓
    Ejecutada cada 300ms mediante window.after()
    ├─ Revisar todas las ventanas abiertas
    ├─ Método helper: _hay_ventanas_bloqueadas()
    │    ├─ ¿Hay alguna ventana abierta (esta_viva()) 
    │    │   Y aún dentro de los 10 segundos (NO cierre_desbloqueado())?
    │    │    ├─ SÍ  → return True
    │    │    └─ NO  → return False
    ├─ Si hay ventanas bloqueadas
    │    └─ close_main_button.configure(state=DISABLED) ← Botón rojo deshabilitado
    └─ Si todas están desbloqueadas
        └─ close_main_button.configure(state=NORMAL) ← Botón rojo habilitado
```

**Archivo relevante**: `app/ui/main_app.py` → métodos `_actualizar_estado_boton_cerrar()` y `_hay_ventanas_bloqueadas()`

### 7. **USUARIO CIERRA UNA VENTANA SECUNDARIA (Después de 10s)**

```
Usuario hace clic en "Cerrar esta ventana" (solo disponible después de 10s)
    ↓
VentanaTema._cerrar_con_boton()
    ├─ window.destroy() (destruir la ventana)
    └─ Llamar callback: on_window_closed(tema_name)
         ↓
         AplicacionPrincipal.al_cerrar_tema(tema_name)
         ├─ ¿Es el tema actualmente activo?
         │    ├─ SÍ  → Buscar otra ventana abierta para mostrar su contador
         │    │       ├─ Si encuentra → active_topic_name = nuevo_tema
         │    │       └─ Si no hay más ventanas → active_topic_name = None
         │    │                                  → Limpiar dashboard (text="")
         │    └─ NO → Solo actualizar estado del botón
         └─ Actualizar estado del botón cerrar
```

**Archivo relevante**: `app/ui/main_app.py` → método `al_cerrar_tema()`

### 8. **INTENTO DE CERRAR LA APLICACIÓN**

```
Usuario hace clic en "Cerrar ventana principal" (botón rojo)
    ↓
    ¿El botón está deshabilitado (hay ventanas bloqueadas)?
    ├─ SÍ  → Ignorar el clic (no hace nada)
    └─ NO  → Continuar...

AplicacionPrincipal.solicitar_cierre()
    ├─ Verificar _hay_ventanas_bloqueadas()
    │    ├─ SÍ  → messagebox("Espera 10 segundos...")
    │    │        └─ Retornar (no cerrar)
    │    └─ NO  → Continuar...
    ├─ Mostrar messageboxOkNo: "¿Deseas cerrar?"
    ├─ ¿Usuario presiona SÍ?
    │    ├─ SÍ  → root.destroy() (cerrar todo)
    │    └─ NO  → Retornar (usuario cambió de opinión)
    └─ Aplicación cierra completamente
```

**Archivo relevante**: `app/ui/main_app.py` → método `solicitar_cierre()`

---

## 🔧 Componentes Principales

### **app/config.py** (Configuración Global)

| Constante | Valor | Propósito |
|-----------|-------|----------|
| `MAIN_SIZE` | "980x620" | Tamaño de la ventana principal |
| `CLOSE_DELAY_SECONDS` | 10 | Duración del bloqueo de cierre |
| `TOPICS` | dict | Mapeo tema → archivo PNG |
| `APP_TITLE` | "Grupo_7SB_Equipo7_..." | Título de la aplicación |

### **app/ui/main_app.py** (AplicacionPrincipal)

Responsabilidades:
- Gestionar la ventana principal y sus componentes
- Coordinar aperturas/cierres de ventanas secundarias
- Mostrar el contador del dashboard (tema activo)
- Controlar el estado del botón de cierre

Métodos principales:
- `_centrar_ventana()`: Centra en pantalla
- `_construir_menu()`: Crea menú desplegable
- `_construir_ui()`: Crea botones y labels
- `abrir_ventana_tema()`: Abre o enfoca una ventana de tema
- `actualizar_contador_principal()`: Actualiza el dashboard
- `al_cerrar_tema()`: Maneja cierre de ventana secundaria
- `_actualizar_estado_boton_cerrar()`: Poll cada 300ms
- `solicitar_cierre()`: Cierre confirmado

### **app/ui/topic_window.py** (VentanaTema)

Responsabilidades:
- Mostrar imagen PNG del tema
- Ejecutar contador de 10 segundos
- Bloquear cierre durante el countdown
- Notificar cambios al dashboard

Métodos principales:
- `_cargar_fondo()`: Carga PNG o muestra error
- `_contar_regresivo()`: Recursión cada 1 segundo
- `_habilitar_boton_cerrar()`: Desbloquea al llegar a 0
- `_al_cerrar_ventana()`: Valida allow_close
- `cierre_desbloqueado()`: Retorna True si seconds_left <= 0
- `esta_viva()`: Verifica si ventana existe

### **app/main.py** (Inicializador)

- Valida que todas las imágenes existan
- Crea instancia de `AplicacionPrincipal`
- Inicia el loop de eventos

---

## 💡 Conceptos Clave

### **Callbacks (Devoluciones de llamada)**

Las ventanas secundarias notifican a la principal mediante callbacks:

```python
# En abrir_ventana_tema()
ventana = VentanaTema(
    ...,
    on_countdown_update=self.actualizar_contador_principal,  ← Callback 1
    on_window_closed=self.al_cerrar_tema                      ← Callback 2
)
```

### **Contador Regresivo No Bloqueante**

Se usa `window.after(ms, function)` para no congelar la interfaz:

```python
def _contar_regresivo(self):
    # ... actualizar contador ...
    self.window.after(1000, self._contar_regresivo)  ← Ejecuta en 1 segundo
```

### **Polling del Estado del Botón**

Cada 300ms se verifica si todas las ventanas están desbloqueadas:

```python
def _actualizar_estado_boton_cerrar(self):
    if self._hay_ventanas_bloqueadas():
        self.close_main_button.configure(state=tk.DISABLED)
    self.root.after(300, self._actualizar_estado_boton_cerrar)  ← Repite cada 300ms
```

---

## 📦 Flujo de Datos

```
                    ┌─────────────────────────┐
                    │  VENTANA PRINCIPAL      │
                    │ (AplicacionPrincipal)   │
                    └────┬────────────┬───────┘
                         │            │
                    Botones tema    Contador dashboard
                         │            │
        ┌────────────────┼────────────┼──────────────────┐
        ↓                ↓            ↑                  ↑
    VentanaTema-1    VentanaTema-2   VentanaTema-3
    (Tema A)         (Tema B)        (Tema C)
    ├─ Contador      ├─ Contador     ├─ Contador
    ├─ Imagen        ├─ Imagen       ├─ Imagen
    └─ Bloqueado     └─ Desbloqueado └─ Contando
       (5s left)        (0s)            (8s left)
```

**La ventana activa (VentanaTema-1) actualiza el dashboard cada segundo.**

---

## 🎮 Manual de Usuario

### Ejecutar la aplicación

```bash
python ventanas.py
```

### Usar la aplicación

1. **Abrir un tema**: Haz clic en cualquier botón azul (Base de Conocimientos, Motor de Inferencia, etc.)
2. **Ver contador**: En el dashboard aparecerá "10s" y decrementará cada segundo
3. **Cambiar tema activo**: Abre otra ventana → el dashboard mostrará su contador
4. **Cerrar ventana secundaria**: Espera 10 segundos → aparecerá botón amarillo → haz clic
5. **Cerrar aplicación**: 
   - Haz clic en el botón rojo "Cerrar"
   - Si hay ventanas bloqueadas → mensaje de espera
   - Si todas desbloqueadas → confirmación → cierra

---

## 🛠️ Configuración Avanzada

Edita `app/config.py` para cambiar:

```python
# Cambiar tamaño principal
MAIN_SIZE = "1024x768"  

# Cambiar tiempo de bloqueo (en milisegundos)
CLOSE_DELAY_MS = 5000  # 5 segundos en lugar de 10

# Agregar nuevos temas
TOPICS = {
    "Mi Nuevo Tema": IMG_DIR / "mi_imagen.png",
    ...
}
```

---

## 📝 Notas Técnicas

- **Framework**: Tkinter (GUI nativa de Python)
- **Imágenes**: PNG (soporte nativo de tk.PhotoImage)
- **Threading**: No se usa (Tkinter ya es single-threaded)
- **Validación**: Se valida existencia de imágenes al iniciar
- **Comportamiento**: Determinista (no hay multihilo)

---

## ✅ Checklist de Funcionalidades

- ✅ 3 ventanas secundarias con temas
- ✅ Contador de 10 segundos per ventana
- ✅ Todas las ventanas centradas en pantalla
- ✅ Dashboard muestra contador del tema activo
- ✅ Botón rojo deshabilitado mientras hay ventanas bloqueadas
- ✅ Validación de imágenes al iniciar
- ✅ Menú con opciones (Recentrar, Cerrar, Equipo)
- ✅ Código documentado en español
- ✅ Estructura modular (fácil de expandir)

---

**Grupo 7 - Carrillo, Ruiz, Salazar** 🎓
