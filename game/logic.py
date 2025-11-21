
from typing import List, Tuple, Dict
import random
from functools import reduce

from game.tutorials import mostrar_tutorial_si_corresponde
from auth.users import guardar_usuario

# Palabras del juego (Hito 1: listas/tuplas)
PALABRAS: Tuple[str, ...] = (
    "casa", "perro", "gato", "café", "mate", "luz", "tecla", "plato", "silla", "salud"
)

LARGO = 5  # Forzamos 5 para tutorial, usaremos slicing si la palabra no lo cumple

class GameError(Exception):
    pass

def _normalizar_palabra(p: str) -> str:
    # Ejemplo de operaciones con cadenas y slicing (Hito 1)
    p = p.lower().strip()
    return p[:LARGO]

def elegir_palabra() -> str:
    # elegimos palabras que tengan al menos LARGO; usamos filter (Hito 2)
    candidatas = list(filter(lambda w: len(w) >= LARGO, PALABRAS))
    if not candidatas:
        raise GameError("No hay palabras válidas para jugar.")
    return random.choice(candidatas)

def evaluar_intento(secreta: str, intento: str) -> List[str]:
    intento = _normalizar_palabra(intento)
    if len(intento) != LARGO:
        raise GameError(f"El intento debe tener {LARGO} letras.")
    marcas: List[str] = []
    # Usamos conjuntos (Hito 1) para validar letras presentes
    presentes = set(secreta)
    for i, ch in enumerate(intento):
        if i < len(secreta) and ch == secreta[i]:
            marcas.append("✓")
        elif ch in presentes:
            marcas.append("~")
        else:
            marcas.append("x")
    return marcas

def imprimir_feedback(intento: str, marcas: List[str]) -> None:
    colores = {
            "✓": "\033[92m",  # Verde (letra correcta en posición correcta)
            "~": "\033[93m",  # Amarillo (letra presente en otra posición)
            "x": "\033[90m",  # Gris (letra incorrecta)
    }
    reset = "\033[0m"
    bloques = [
            f"{colores.get(m, '')}{c.upper()}{reset}"
     for c, m in zip(intento, marcas)
    ]
    print(" ".join(bloques))

  # Además mostramos leyenda la primera vez
    print("\033[92m✓ Correcta\033[0m | \033[93m~ Presente\033[0m | \033[90mx Incorrecta\033[0m")

def jugar(user: Dict) -> None:
    mostrar_tutorial_si_corresponde(user, "inicio_juego")
    secreta = elegir_palabra()
    # aseguramos largo con slicing
    secreta = secreta[:LARGO]
    intentos_max = 6
    intentos: List[str] = []

    for intento_num in range(1, intentos_max + 1):
        mostrar_tutorial_si_corresponde(user, "ingreso_intento")
        intento = input(f"Intento {intento_num}/{intentos_max}: ").strip().lower()
        try:
            marcas = evaluar_intento(secreta, intento)
        except GameError as e:
            print(f"Error: {e}")
            continue
        imprimir_feedback(intento[:LARGO], marcas)
        intentos.append(intento[:LARGO])
        if all(m == "✓" for m in marcas):
            print("¡Adivinaste!")
            user["progress"]["wins"] += 1
            break
    user["progress"]["games"] += 1
    guardar_usuario(user)
    mostrar_estadisticas(user, intentos)

def mostrar_estadisticas(user: Dict, intentos: List[str]) -> None:
    mostrar_tutorial_si_corresponde(user, "estadisticas")
    juegos = user["progress"]["games"]
    wins = user["progress"]["wins"]
    # reduce para calcular total de letras ingresadas (Hito 2)
    total_letras = reduce(lambda acc, w: acc + len(w), intentos, 0)
    ratio = (wins / juegos) if juegos else 0.0
    print(f"Partidas: {juegos} | Victorias: {wins} | Ratio: {ratio:.2f} | Letras tipeadas: {total_letras}")
