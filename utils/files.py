
from typing import Any, Dict, List
import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.txt")

def ensure_data_files() -> None:
    """Create data files if they don't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            f.write("")

def read_users() -> List[Dict[str, Any]]:
    """Read JSONL users from users.txt."""
    ensure_data_files()
    users: List[Dict[str, Any]] = []
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                users.append(json.loads(line))
            except json.JSONDecodeError:
                # Skip malformed lines but keep file resilient
                continue
    return users

def write_users(users: List[Dict[str, Any]]) -> None:
    """Persist JSONL users to users.txt safely."""
    ensure_data_files()
    tmp_path = USERS_FILE + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        for u in users:
            f.write(json.dumps(u, ensure_ascii=False) + "\n")
    os.replace(tmp_path, USERS_FILE)
