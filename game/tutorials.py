
from typing import Dict, Callable
from auth.users import guardar_usuario

# Diccionario (Hito 1) con los tutoriales del juego
TUTORIALES: Dict[str, str] = {
    "inicio_juego": "Bienvenido. Tu objetivo es adivinar la palabra en 6 intentos.",
    "ingreso_intento": "Ingresa una palabra de 5 letras. Las letras correctas en posición se marcan como [✓], presentes fuera de posición como (~).",
    "estadisticas": "Aquí verás tus estadísticas: partidas, victorias y ratio de éxito.",
}

def mostrar_tutorial_si_corresponde(user: dict, clave: str) -> None:
    vistos = user.get("tutoriales_hechos", set())
    if clave not in vistos:
        print("\n=== Tutorial ===")
        print(TUTORIALES.get(clave, "Sin tutorial disponible."))
        print("================\n")
        # marcamos como visto y persistimos
        vistos.add(clave)
        user["tutoriales_hechos"] = vistos
        guardar_usuario(user)
