from typing import Optional
from auth.users import flujo_login_interactivo, flujo_registro_interactivo
from auth.users import guardar_usuario
from game.logic import jugar

def menu(user: Optional[dict]) -> Optional[dict]:
    print("\n=== MENÚ PRINCIPAL ===")
    if user:
        print(f"Usuario logueado: {user['username']}")
    print("[1] Registrarse")
    print("[2] Iniciar sesión")
    print("[3] Jugar")
    print("[4] Ver progreso")
    print("[0] Salir")
    try:
        op = int(input("Elija una opción: ").strip())
    except ValueError:
        print("Opción inválida.")
        return user

    if op == 1:
        user = flujo_registro_interactivo()
        return user
    elif op == 2:
        user = flujo_login_interactivo()
        return user
    elif op == 3:
        if not user:
            print("Debe iniciar sesión primero.")
        else:
            jugar(user)
        return user
    elif op == 4:
        if not user:
            print("Debe iniciar sesión primero.")
        else:
            p = user["progress"]
            print(f"Juegos: {p['games']} | Victorias: {p['wins']}")
        return user
    elif op == 0:
        return None
    else:
        print("Opción desconocida.")
        return user

def main() -> None:
    print("Bienvenido al Mini Wordle 🧩")
    user: Optional[dict] = None
    while True:
        user = menu(user)
        if user is None:
            print("¡Hasta la próxima!")
            break
        # persistimos cambios en cada vuelta por si el menú actualizó algo
        guardar_usuario(user)

if __name__ == "__main__":
    main()
