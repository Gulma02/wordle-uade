
import os
import unittest
from utils.files import DATA_DIR, USERS_FILE, write_users
from auth.users import registrar_usuario, login

class TestAuth(unittest.TestCase):
    def setUp(self):
        # reset file
        os.makedirs(DATA_DIR, exist_ok=True)
        open(USERS_FILE, "w").close()

    def test_registro_y_login(self):
        u = registrar_usuario("juan_1", "pass1")
        self.assertEqual(u["username"], "juan_1")
        ok = login("juan_1", "pass1")
        self.assertIsNotNone(ok)

if __name__ == "__main__":
    unittest.main()
