from miasta import Miasta
import tkinter as tk
from tkinter import ttk

if __name__ == '__main__':
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

    # Inicjalizacja okna
    root = tk.Tk()
    root.geometry('600x700')
    root.title("Stacje pomiarowe")

    # Okno z błędami
    bledy = tk.Label(root,text = "W razie wystąpienia błędów \n pojawią się one tutaj")
    bledy.grid(row=7,column=2,padx=15,pady=15,sticky="s")

    # Etykieta dla wyboru miasta
    label_miasta = tk.Label(root, text="Wybierz miasto")
    label_miasta.grid(row=1, column=1, padx=10, pady=10)

    #Obiekt klasy Miasta
    miasta = Miasta()
    miasta.download_all_cities(bledy)

    # Lista rozwijana (Combobox) dla wyboru miasta
    c1 = ttk.Combobox(root, values=miasta.wszystkie_miasta)
    c1.set("wybierz miasto")
    c1.grid(row=2, column=1, padx=10, pady=10)

    # Utworzenie etykiety po prawej stronie
    label = tk.Label(root, text="Wpisz wartości długości i szerokości geograficznej:")
    label.grid(row=1, column=2, padx=10, pady=10, sticky="e")

    # Stworzenie ramki dla pierwszego i drugiego pola
    frame1 = tk.Frame(root)
    frame1.grid(row=2, column=2, padx=10, pady=10)
    frame2 = tk.Frame(root)
    frame2.grid(row=3, column=2, padx=10, pady=10)

    # Dodanie tekstu i pola do ramki
    label1 = tk.Label(frame1, text="Długość:   ")
    label1.pack(side="left")
    entry1 = tk.Entry(frame1, width=20)
    entry1.pack(side="left")
    label2 = tk.Label(frame2, text="Szerokość:")
    label2.pack(side="left")
    entry2 = tk.Entry(frame2, width=20)
    entry2.pack(side="left")

    # Przycisk do zatwierdzenia wyboru miasta
    przycisk_miasto = tk.Button(root, text="Zatwierdź miasto",command= lambda:[miasta.choose_city(c1,c2,przycisk_adres,bledy),miasta.choose_adres_in_city(c2)])
    przycisk_miasto.grid(row=3, column=1, padx=10, pady=10)

    # Druga lista rozwijana (Combobox) do wyboru adresu w mieście - początkowo pusty
    c2 = ttk.Combobox(root)
    c2.set("wybierz adres")

    # Przycisk zatwuerdzający adres konkretnego czujnika
    przycisk_adres = tk.Button(root, text="Zatwierdź adres",command= lambda: miasta.choose_one_address(c2,c3,przycisk_zanieczyszczenia,bledy))

    # Trzeci combobox do wyboru zanieczyszczenia
    c3 = ttk.Combobox(root)
    c3.set("wybierz zanieczyszczenie")

    # Przycisk zatwierdzający zanieczyszczenie
    przycisk_zanieczyszczenia = tk.Button(root, text = "Zatwierdź zanieczyszczenie \n i utwórz bazę danych", command = lambda: [miasta.choose_contamination(c3,bledy),miasta.make_database(przycisk_wykres,bledy)])

    # Tabela z danymi statystycznymi - początkowo pusta
    table_statistic = ttk.Treeview(root)

    # Przycisk otwierający nowe okno z wyrysowanym wykresem
    przycisk_wykres = tk.Button(root, text = "Rysuj wykres \n i wyświetl statystykę",command = lambda: [miasta.draw_plot(plot_window), miasta.statistics(table_statistic)])

    # Przycisk zatwierdzający podane wartości długości i szerokości geograficznej, który wyświetla wynik i adres najbliższej stacji
    przycisk_dlszer = tk.Button(root, text="Zatwierdź",command= lambda: miasta.get_input(entry1,entry2,wynik_obliczen,bledy))
    przycisk_dlszer.grid(row=4, column=2, padx=10, pady=10)

    # Okno wyświetlające wynik najbliższej stacji - początkowo puste
    wynik_obliczen = tk.Label(root,text="Instrukcja: \n Poddaj liczby, aby dowiedzieć się,\n gdzie jest najbliższa stacja pomiarowa")
    wynik_obliczen.grid(row=5, column=2, padx=10, pady=10)

    # Tworzenie nowego okna i jego ukrycie
    plot_window = tk.Toplevel(root)
    plot_window.title("Wykres")
    plot_window.withdraw()

    # Główna pętla aplikacji
    root.mainloop()



