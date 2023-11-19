import random
import numpy as np
from tkinter import messagebox

XDDDD

# Definicja klasy Cząsteczki
class Cząsteczka:
    # Wywołanie automatyczne podczas tworzenia nowego obiektu klasy 'Cząsteczka'
    def __init__(self, pozycja):
        # Przechowanie aktualnej pozycji cząsteczki w przestrzeni poszukiwań
        self.pozycja = pozycja
        # Inicjalizacja prędkości cząsteczki jako wektora o zerowych wartościach, ale tej samej długości co wymiar pozycji
        self.prędkość = np.zeros_like(pozycja)
        # Przechowanie informacji o najlepszej dotychczas znalezionej pozycji
        self.najlepsza_pozycja = pozycja
        # Inicjalizacja najlepszej zananej wartości dla cząsteczki jako nieskończoność
        self.najlepsza_wartość = float('inf')

def PSO(Funkcja_Oceny, Rozmiar_Populacji, D, MaxIteracje):
    # Inicjalizacja globalnej najlepszej znalezionej pozycji
    globalna_najlepsza_pozycja = None
    # Inicjalizacja globalnej najlepszej wartości jako nieskończoność
    globalna_najlepsza_wartość = float('inf')
    # Inicjalizacja listy cząsteczek
    cząsteczki = []

    # Inicjalizacja pierwszej pozycji i cząsteczki

    # Losowanie początkowej pozycji w przestrzeni poszukiwań
    pozycja = np.random.uniform(-0.5, 0.5, D)
    # Tworzenie pierwszej cząsteczki z początkową pozycją
    cząsteczka = Cząsteczka(pozycja)
    # Dodanie cząsteczki do listy
    cząsteczki.append(cząsteczka)

    #Aktualizacja wartości na podstawie początkowej pozycji

    # Obliczenie wartości funkcji dla początkowej pozycji
    wartość = Funkcja_Oceny(pozycja)
    if wartość < globalna_najlepsza_wartość:
        # Aktualizacja globalnej najlepszej wartości
        globalna_najlepsza_wartość = wartość
        # Aktualizacja globalnej najlepszej pozycji
        globalna_najlepsza_pozycja = pozycja

        # Aktualizacja najlepszej pozycji cząsteczki
        cząsteczka.najlepsza_pozycja = pozycja
        # Aktualizacja najlepszej wartości cząsteczki
        cząsteczka.najlepsza_wartość = wartość

    # Główna pętla algorytmu PSO
    for iteracja in range(MaxIteracje):
        for cząsteczka in cząsteczki:
            # Aktualizacja prędkości cząsteczki
            # Waga inercji cząsteczki; kontroluje wpływ aktualnej prędkości na przyszłą prędkość
            w = 0.8
            # Współczynnik kognitywny; kontroluje wpływ najlepszej dotychczasowej pozycji cząsteczki na aktualizację jej prędkości
            c1 = 1.2
            # Współczynnik społeczny; kontroluje wpływ globalnej najlepszej pozycji w całej populacji na aktualizację prędkości cząsteczki
            c2 = 1.2

            r1 = random.random()
            r2 = random.random()

            # Obliczenie prędkości cząsteczki
            cząsteczka.prędkość = (
                w * cząsteczka.prędkość +
                c1 * r1 * (cząsteczka.najlepsza_pozycja - cząsteczka.pozycja) +
                c2 * r2 * (globalna_najlepsza_pozycja - cząsteczka.pozycja)
            )

            # Aktualizacja pozycji cząsteczki na podstawie prędkości
            cząsteczka.pozycja += cząsteczka.prędkość

            # Ocena funkcji dla nowej pozycji
            wartość = Funkcja_Oceny(cząsteczka.pozycja)

            # Aktualizacja najlepszej pozycji dla cząsteczki, jeśli jest lepsza
            if wartość < cząsteczka.najlepsza_wartość:
                cząsteczka.najlepsza_wartość = wartość
                cząsteczka.najlepsza_pozycja = cząsteczka.pozycja

            # Aktualizacja globalnie najlepszej pozycji i wartości
            if wartość < globalna_najlepsza_wartość:
                globalna_najlepsza_wartość = wartość
                globalna_najlepsza_pozycja = cząsteczka.pozycja

    # Zwraca globalnie najlepszą pozycję i wartość
    return globalna_najlepsza_pozycja, globalna_najlepsza_wartość


# Definicja funkcji oceny

# Obliczenie sumy kwadratów elementów wektora x
def Funkcja_testowa1(x):
    return np.sum(x**2)

# Obliczenie maksymalnej wartości bezwzględnej elementów wektora x
def Funkcja_testowa2(x):
    return np.max(np.abs(x))

# Przechowywanie funkcji oceny w słowniku Funkcje_Oceny
Funkcje_Oceny = {'Funkcja_testowa1': Funkcja_testowa1, 'Funkcja_testowa2': Funkcja_testowa2}

# Parametry

# Liczba cząsteczek w populacji
Rozmiar_Populacji = 200
# Maksymalna liczba iteracji algorytmu
MaxIteracje = 100
# Wymiarowość problemu (ilość wymiarów przestrzeni rozwiązań)
D = 2

# Iteracja po każdej funkcji oceny i uruchomienie PSO
for nazwa_funkcji, Funkcja_Oceny in Funkcje_Oceny.items():
    # Informacja o obecnie testowanej funkcji
    Wynik = "Uruchamianie Funkcji = " + nazwa_funkcji + "\n"
    # Uruchomienie algorytmu PSO dla danej funkcji oceny
    najlepsza_pozycja, najlepsza_wartość = PSO(Funkcja_Oceny, Rozmiar_Populacji, D, MaxIteracje)
    # Wyświetlenie najlepszej znalezionej pozycji
    Wynik += "NAJLEPSZA POZYCJA: " + str(najlepsza_pozycja) + "\n"
    # Wyświetlenie najlepszej znalezionej wartości
    Wynik += "NAJLEPSZA WARTOŚĆ: " + str(najlepsza_wartość)
    Wynik += "\n"

    # Wyświetlenie okna dialogowego z wynikami dla każdej funkcji oceny
    messagebox.showinfo("PSO RUN", Wynik)
