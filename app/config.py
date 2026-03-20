from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "imgs"

# CONFIGURACION RAPIDA
MAIN_SIZE = "980x620"
MAIN_MIN_WIDTH = 900
MAIN_MIN_HEIGHT = 560
APP_TITLE = "Grupo_7SB_Equipo7_Carrillo Ruiz Salazar"

CHILD_SIZE_FACTOR = 0.62
CHILD_MIN_WIDTH = 360
CHILD_MIN_HEIGHT = 240
CHILD_OFFSET_X = 80
CHILD_OFFSET_Y = 70

# 10 segundos para mostrar el boton de cierre de cada secundaria.
CLOSE_DELAY_MS = 10000
CLOSE_DELAY_SECONDS = CLOSE_DELAY_MS // 1000

TOPICS = {
    "Base de Conocimientos": IMG_DIR / "base_de_conocimientos.png",
    "Motor de Inferencia": IMG_DIR / "motor_de_inferencia.png",
    "Interfaz de Usuario": IMG_DIR / "interfaz_de_usuario.png",
}


def validar_imagenes() -> list[str]:
    """Regresa una lista con las rutas faltantes esperadas por la app."""
    faltantes = []
    for ruta in TOPICS.values():
        if not ruta.exists():
            faltantes.append(str(ruta))
    return faltantes
