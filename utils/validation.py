
import re

USERNAME_RE = re.compile(r"^[a-zA-Z0-9_]{3,15}$")
PASSWORD_RE = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*()_+\-=\[\]{};':\",.<>/?]{4,}$")

def validar_username(nombre: str) -> bool:
    return bool(USERNAME_RE.match(nombre))

def validar_password(pw: str) -> bool:
    # At least 4 chars, contain letters and numbers (simple check)
    return bool(PASSWORD_RE.match(pw))
