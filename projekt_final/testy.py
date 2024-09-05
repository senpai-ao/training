import unittest
from unittest.mock import MagicMock
from miasta import Miasta

class Test(unittest.TestCase):
    """
    Klasa zawierająca przykładowe testy dotyczące funkcji get_input z klasy Miasta
    """
    miasta=Miasta()

    def test_get_input_invalid_entry2(self):
        """
        Test ten dotyczy przypadku, gdy podamy dwie niepoprawne wartości - string zamiast float
        """
        # Przygotowanie fałszywych pól entry
        entry1 = MagicMock()
        entry2 = MagicMock()

        # Ustawienie zwracanych wartości jako stringi
        entry1.get.return_value = "abc"  # Niepoprawna wartość
        entry2.get.return_value = "xyz"  # Nieoprawna wartość

        # Mock dla obiektów wynik_obliczen i bledy
        wynik_obliczen = MagicMock()
        bledy = MagicMock()

        # Wywołanie funkcji
        self.miasta.get_input(entry1, entry2, wynik_obliczen, bledy)

        # Sprawdzenie, czy błąd został obsłużony prawidłowo
        bledy.config.assert_called_with(text="Należy podać wartości liczbowe!")  # Sprawdzamy, czy komunikat błędu został wywołany
        wynik_obliczen.config.assert_not_called()  # Upewniamy się, że wynik nie został ustawiony, bo dane są błędne

    def test_get_input_invalid_entry1(self):
        """
        Test ten dotyczy przypadku, gdy podamy dwie jedną niepoprawną wartość - string zamiast float
        """
        # Przygotowanie fałszywych pól entry
        entry1 = MagicMock()
        entry2 = MagicMock()

        # Ustawienie zwracanych wartości jako stringi
        entry1.get.return_value = "abc"  # Niepoprawna wartość
        entry2.get.return_value = 20.0  # Poprawna wartość

        # Mock dla obiektów wynik_obliczen i bledy
        wynik_obliczen = MagicMock()
        bledy = MagicMock()

        # Wywołanie funkcji
        self.miasta.get_input(entry1, entry2, wynik_obliczen, bledy)

        # Sprawdzenie, czy błąd został obsłużony prawidłowo
        bledy.config.assert_called_with(text="Należy podać wartości liczbowe!")  # Sprawdzamy, czy komunikat błędu został wywołany
        wynik_obliczen.config.assert_not_called()  # Upewniamy się, że wynik nie został ustawiony, bo dane są błędne


if __name__ == '__main__':
    unittest.main()