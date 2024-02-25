import unittest
from unittest.mock import patch
import os
from dotenv import load_dotenv
import sys
from io import StringIO

from src.main import App

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()  

        cls.TICKETS = int(os.getenv("TICKETS"))
        cls.T_MAX = int(os.getenv("T_MAX"))
        cls.T_MIN = int(os.getenv("T_MIN"))

    def setUp(self):
        self.app = App()

    def test_init_app(self):
        self.assertEqual(self.app.TICKETS, self.TICKETS)
        self.assertEqual(self.app.T_MAX, self.T_MAX)
        self.assertEqual(self.app.T_MIN, self.T_MIN)

    @patch('requests.get')  # Simulez 'requests.get' pour la durée de ce test
    def test_send_action_to_hvac(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"Response": "Activating AC for 2 TICKETS"}
        self.app.send_action_to_hvac("TurnOnAc")
        mock_get.assert_called_once()

    def test_take_action_at_max(self):
        output = self.get_print(self.app.take_action, self.T_MAX)
        self.assertIn("Turning on AC.", output)

    def test_take_action_at_min(self):
        output = self.get_print(self.app.take_action, self.T_MIN)
        self.assertIn("Turning on Heater.", output)

    def test_take_action_over_max(self):
        output = self.get_print(self.app.take_action, self.T_MAX + 1)
        self.assertIn("Turning on AC.", output)

    def test_take_action_under_min(self):
        output = self.get_print(self.app.take_action, self.T_MIN - 1)
        self.assertIn("Turning on Heater.", output)

    def get_print(self, action, *args):
        # Sauvegardez la sortie standard
        original_stdout = sys.stdout
        # Redirigez stdout vers un StringIO pour capturer les impressions
        sys.stdout = StringIO()
        action(*args)
        # Récupérez la sortie de la fonction
        output = sys.stdout.getvalue().strip()
        # Restaurez la sortie standard
        sys.stdout = original_stdout
        return output

if __name__ == "__main__":
    unittest.main()
