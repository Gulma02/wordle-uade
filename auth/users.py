
from typing import Dict, List, Any, Optional
from getpass import getpass
from utils.files import read_users, write_users
from utils.validation import validar_username, validar_password

class AuthError(Exception):
    pass

def _index_by_username(users: List[Dict[str, Any]]) -> Dict[str, int]:
    return {u["username"]: i for i, u in enumerate(users)}

def registrar_usuario(username: str, password: str) -> Dict[str, Any]:
    users = read_users()
    index = _index_by_username(users)
    if not validar_username(username):
        raise AuthError("Nombre de usuario inválido. Use 3-15 chars [a-zA-Z0-9_].")
    if not validar_password(password):
        raise AuthError("Contraseña inválida. Debe incluir letras y números (mín 4).")
    if username in index:
        raise AuthError("El usuario ya existe.")
    nuevo = {
        "username": username,
        "password": password,  # Para demo. En producción, usar hashing.
        "progress": {"games": 0, "wins": 0},
        "tutoriales_hechos": []  # se guarda como lista, lo usaremos como set en memoria
    }
    users.append(nuevo)
    write_users(users)
    return nuevo

def login(username: str, password: str) -> Optional[Dict[str, Any]]:
    for u in read_users():
        if u["username"] == username and u["password"] == password:
            # Normalizamos tipos
            u["tutoriales_hechos"] = set(u.get("tutoriales_hechos", []))
            return u
    return None

def guardar_usuario(user: Dict[str, Any]) -> None:
    users = read_users()
    index = _index_by_username(users)
    user_to_save = dict(user)
    # set -> list for json
    if isinstance(user_to_save.get("tutoriales_hechos"), set):
        user_to_save["tutoriales_hechos"] = list(user_to_save["tutoriales_hechos"])
    if user_to_save["username"] not in index:
        users.append(user_to_save)
    else:
        users[index[user_to_save["username"]]] = user_to_save
    write_users(users)

def flujo_registro_interactivo() -> Dict[str, Any]:
    print("== Registro de usuario ==")
    username = input("Nombre de usuario: ").strip()
    password = getpass("Contraseña: ").strip()
    try:
        user = registrar_usuario(username, password)
        # Convertimos lista -> set para uso en runtime
        user["tutoriales_hechos"] = set(user.get("tutoriales_hechos", []))
        print("Usuario creado con éxito.")
        return user
    except AuthError as e:
        print(f"Error: {e}")
        return flujo_registro_interactivo()

def flujo_login_interactivo() -> Optional[Dict[str, Any]]:
    print("== Inicio de sesión ==")
    username = input("Usuario: ").strip()
    password = getpass("Contraseña: ").strip()
    user = login(username, password)
    if user:
        print(f"¡Bienvenido {username}!")
        return user
    print("Usuario o contraseña incorrectos.")
    # Ejemplo de recursividad para reintentar
    retry = input("¿Reintentar? (s/n): ").strip().lower()
    if retry == "s":
        return flujo_login_interactivo()
    return None
