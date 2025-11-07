
import unittest
from game.logic import evaluar_intento

class TestGame(unittest.TestCase):
    def test_evaluar(self):
        r = evaluar_intento("casae", "cable")
        self.assertEqual(len(r), 5)
        self.assertTrue(all(m in ["✓","~","x"] for m in r))

if __name__ == "__main__":
    unittest.main()
