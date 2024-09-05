import requests
import sqlite3
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import statistics
import time

class Miasta:
    """
    Klasa zawierająca wszystkie wymagane operacje do pobierania i wczytywania danych, tworzenia
    baz danych, przeprowadzania obliczeń statystycznych,
    """

    def __init__(self):
        self.wybrane_miasto = None
        self.wybrane_adresy = None
        self.adres = None
        self.zanieczyszczenie = None
        self.wszystkie_miasta = []
        self.nazwa_miasta = None
        self.dlugosc = None
        self.szerokosc = None
        self.stacje_json = {}
        self.wskazniki_json = None
        self.zanieczyszczenie_json = None
        self.pojedyncza_baza = None
        self.lokacje_df = []
        self.wynik = None


    def download_all_cities(self,bledy):
        """
        Funkcja pobierająca dane z API, jak również:
        - lewa część aplikacji - pobierania nazw miast i zapisywania ich w zmiennej self
        - prawa część aplikacji - tworzenie DataFrame'u z nazwą stacji, szerokością i długością geograficzną stacji

        Dodatkowo funkcja została wyposażona w możliwość sprawdzenia połączenia z internetem.
        """
        try:
            self.stacje = requests.get('https://api.gios.gov.pl/pjp-api/rest/station/findAll',timeout=5)
            self.stacje_json = self.stacje.json()
            for slownik in self.stacje_json:
                city = slownik.get("city", {}).get("name", {})
                self.wszystkie_miasta.append(city)
            self.wszystkie_miasta = sorted(list(set(self.wszystkie_miasta)))

            #do prawej części gui
            polozenia = []
            for slownik in self.stacje_json:
                polozenie = [slownik.get("stationName",{}),slownik.get("gegrLat",{}),slownik.get('gegrLon',{})]
                polozenia.append(polozenie)
            self.lokacje_df = pd.DataFrame(polozenia,columns=["Nazwa_stacji","Szerokosc_geo","Dlugosc_geo"])

        except requests.exceptions.ConnectionError:
            bledy.config(text="Brak połączenia z internetem. Ponowna próba połączenia za 20 sekund")
            time.sleep(20)
            self.download_all_cities(bledy)
        except requests.exceptions.Timeout:
            bledy.config(text="Czas oczekiwania na odpowiedź serwera upłynął.")
            time.sleep(20)





    def choose_city(self,c1,c2,przycisk_adres,bledy):
        """
        Funkcja pobierająca wybór użytkownika z c1 i wyśweitlająca c2 i przycisk_adres

        Args:
            param c1: combobox z listą miast
            param c2: combobox z listą adresów w wybranym mieście
            param przycisk_adres: przycisk wybierający adres z combobox 2

        """
        try:
            self.wybrane_miasto = c1.get()
            if self.wybrane_miasto == 'wybierz miasto':
                raise ValueError("Combobox jest pusty")

            c2.grid(row=6, column=1, padx=10, pady=10)
            przycisk_adres.grid(row=7, column=1, padx=10, pady=10)
        except ValueError:
            c2.grid_remove()
            przycisk_adres.grid_remove()
            bledy.config(text="Nie wybrano miasta z listy rozwijanej!")



    def choose_adres_in_city(self,c2):
        """
        Funkcja pobierająca adresy dla danego miasta ze słownika i przekazująca je do c2

        Args:
            param c2: combobox z listą adresów w wybranym mieście

        """
        self.wybrane_adresy = [slownik['stationName'] for slownik in self.stacje_json if slownik['city']['name'] == self.wybrane_miasto]
        c2['values'] = self.wybrane_adresy

    def choose_one_address(self,c2,c3,przycisk_zanieczyszczenia,bledy):
        """
        Funkcja pobierająca informacje o wybranym adresie z combobox 2,
        pobierająca z API informacje o mierzonych zanieczyszczeniach,
        przekazująca je do c3 i wyświetlająca c3 oraz przycisk_zanieczyszczenia

        Args:
            param c2: combobox z listą adresów w wybranym mieście
            param c3: combobox z listą zanieczyszczeń mierzonych przez wybraną stację
            param przycisk_zanieczyszczenia: przycisk wybierający zanieczyszczenia z combobox 3 i tworzący bazę

        """
        try:
            self.adres = c2.get()
            if self.adres == "wybierz adres":
                raise ValueError("Combobox jest pusty")

            wybrany_id_z_adresu = [slownik['id'] for slownik in self.stacje_json if slownik['stationName'] == self.adres]
            wybrany_id_z_adresu = str(wybrany_id_z_adresu).replace('[', '').replace(']', '').replace("'", "")
            wskazniki = requests.get(f'https://api.gios.gov.pl/pjp-api/rest/station/sensors/{wybrany_id_z_adresu}')
            self.wskazniki_json = wskazniki.json()
            lista_wskaznikow = [slownik['param']['paramName'] for slownik in self.wskazniki_json]
            c3['values'] = lista_wskaznikow
            c3.grid(row=8, column=1, padx=10, pady=10)
            przycisk_zanieczyszczenia.grid(row=9, column=1, padx=10, pady=10)
        except ValueError:
            c3.grid_remove()
            przycisk_zanieczyszczenia.grid_remove()
            bledy.config(text="Nie wybrano adresu z listy rozwijanej!")

    def choose_contamination(self,c3,bledy):
        """
        Funkcja pobierająca informacje o wybranym zanieczyszczeniu z combobox 3 i na podstawie tego
        pobierająca z API dokładnie zmierzone wartości

        Args:
            param c3: combobox z listą zanieczyszczeń mierzonych przez wybraną stację

        """
        try:
            self.zanieczyszczenie = c3.get()
            if self.zanieczyszczenie == "wybierz zanieczyszczenie":
                raise ValueError("Combobox jest pusty")

            id_parametru = [slownik['id'] for slownik in self.wskazniki_json if slownik['param']['paramName'] == self.zanieczyszczenie]
            id_parametru = str(id_parametru).replace('[', '').replace(']', '').replace("'", "")
            zanieczyszczenie_api = requests.get(f'https://api.gios.gov.pl/pjp-api/rest/data/getData/{id_parametru}')
            self.zanieczyszczenie_json = zanieczyszczenie_api.json()
        except ValueError:
            bledy.config(text="Nie wybrano zanieczyszczenia z listy rozwijanej!")

    def make_database(self,przycisk_wykres,bledy):
        """
        Funkcja tworząca bazę danych dla wybranej stacji w wybranym mieście i wybranego zanieczyszczenia,
        a także wyświetlająca przycisk do tworzenia wykresu.

        Args:
            param przycisk_wykres: przycisk zatwierdzający rysowanie wykresu wykorzystując dane z utworzonej bazy

        """
        try:
            conn = sqlite3.connect(f'baza_{self.zanieczyszczenie}_{self.adres}.db')
            cursor = conn.cursor()
            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS contaminations (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            date TEXT,
                            value REAL
                        )
                        ''')
            for entry in self.zanieczyszczenie_json['values']:
                cursor.execute('''
                            INSERT INTO contaminations (date, value)
                            VALUES (?, ?)
                            ''', (entry['date'], entry['value']))

            cursor.execute(f'''
                        DELETE FROM contaminations
                        WHERE value IS NULL
                        ''')
            conn.commit()
            conn.close()
            przycisk_wykres.grid(row=10, column=1, padx=10, pady=10)
        except ValueError:
            bledy.config(text="Nie wybrano zaneczyszczenia!")

    def draw_plot(self,plot_window):
        """
        Funkcja wyświetlająca wykres w nowym oknie wykorzystująca utworzoną bazę danych

        Args:
            param plot_window: okno z wykresem

        """
        conn = sqlite3.connect(f'baza_{self.zanieczyszczenie}_{self.adres}.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM contaminations")
        x = [row[0] for row in cursor.fetchall()]
        x = np.array(x)
        cursor.execute("SELECT value FROM contaminations")
        y = [row[0] for row in cursor.fetchall()]
        y = np.array(y)
        plot_window.deiconify()
        fig = Figure(figsize=(5, 4), dpi=100)
        plot = fig.add_subplot(111)
        plot.plot(x, y)
        a,b = np.polyfit(x, y, 1)
        plot.plot(x,a*x+b)
        plot.set_xlabel("Punkty czasowe")  # Opis osi X
        plot.set_ylabel("Wartość zanieczyszczenia")  # Opis osi Y
        plot.set_title(self.zanieczyszczenie)
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
        conn.close()


    def get_input(self,entry1,entry2,wynik_obliczen,bledy):
        """
        Funkcja dla prawej części aplikacji, pobierająca informacje od użytkownika o długości i szerokości geograficznej
        i obliczqjąca najbliżej dostępną stację pomiarową i wyświetlająca informacje

        Args:
            param entry1: podana wartość długości geograficznej
            param entry2: podana wartość szerokości geograficznej
            param wynik_obliczen: okno wyświetlające wynik

        """
        try:
            self.lokacje_df["Podana Dlugosc"] = float(entry1.get())
            self.lokacje_df["Podana Szerokosc"] = float(entry2.get())
            if isinstance(self.lokacje_df["Podana Dlugosc"], str)  or isinstance(self.lokacje_df["Podana Szerokosc"], float):
                raise ValueError("Podana wartość jest stringiem!")

            self.lokacje_df["Dlugosc_geo"] = self.lokacje_df["Dlugosc_geo"].astype(float)
            self.lokacje_df["Szerokosc_geo"] = self.lokacje_df["Szerokosc_geo"].astype(float)
            self.lokacje_df["Calc"] = np.sqrt(np.abs( self.lokacje_df["Podana Dlugosc"] - (self.lokacje_df["Dlugosc_geo"]))**2 + np.abs(self.lokacje_df["Podana Szerokosc"]-(self.lokacje_df["Szerokosc_geo"]))**2)
            pd.set_option('display.max_columns', None)
            self.wynik = min(self.lokacje_df["Calc"])
            wynik_miasto = self.lokacje_df.loc[self.lokacje_df['Calc'] == self.wynik, 'Nazwa_stacji'].iloc[0]
            wynik_obliczen.config(text=f'Najbliższa stacja {wynik_miasto} \n znajduje się w odległości {round(self.wynik,3)} km')
            wynik_obliczen.grid(row=6, column=2, padx=10, pady=10)
        except ValueError:
            bledy.config(text="Należy podać wartości liczbowe!")


    def statistics(self,table_statistic):
        """
        Funkcja obliczająca podstawowe dane statystyczne odczytane z danych wyświetlanych na wykresie:
        * wartość maksymalna
        * wartość minimalna
        * wartość średnia
        * mediana
        * wariancja

        Args:
            param table_statistic: okno wyświetlające tabelę z danymi statystycznymi

        """
        table_statistic.config(columns=("Cecha", "Wartość"), show="headings")
        table_statistic.heading("Cecha", text="Cecha")
        table_statistic.heading("Wartość", text="Wartość")
        conn = sqlite3.connect(f'baza_{self.zanieczyszczenie}_{self.adres}.db')
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM contaminations")
        values_all = [row[0] for row in cursor.fetchall()]
        labels = ["Maksimum", "Minimum", "Średnia", "Mediana", "Wariancja"]
        values = [max(values_all),min(values_all),round(statistics.mean(values_all),2), round(statistics.median(values_all),2), round(statistics.variance(values_all),2)]
        for label, value in zip(labels, values):
            table_statistic.insert("", "end", values=(label, value))

        table_statistic.grid(row=11,column=1, padx=10, pady=10)

