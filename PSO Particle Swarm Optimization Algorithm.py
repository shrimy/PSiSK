import random
import numpy as np
import matplotlib.pyplot as plt


# Definicja klasy Cząsteczki
class Cząsteczka:
    def __init__(self, pozycja):
        self.pozycja = pozycja
        self.prędkość = np.zeros_like(pozycja)
        self.najlepsza_pozycja = pozycja
        self.najlepsza_wartość = float('inf')

# Funkcja optymalizacji PSO
def PSO(Funkcja_próbna, Rozmiar_Populacji, D, MaxIteracje):
    globalna_najlepsza_pozycja = None
    globalna_najlepsza_wartość = float('inf')
    cząsteczki = []

    pozycja = np.random.uniform(-0.5, 0.5, D)
    cząsteczka = Cząsteczka(pozycja)
    cząsteczki.append(cząsteczka)

    wartość = Funkcja_próbna(pozycja)
    if wartość < globalna_najlepsza_wartość:
        globalna_najlepsza_wartość = wartość
        globalna_najlepsza_pozycja = pozycja

        cząsteczka.najlepsza_pozycja = pozycja
        cząsteczka.najlepsza_wartość = wartość

    for iteracja in range(MaxIteracje):
        for cząsteczka in cząsteczki:
            w = 0.8
            c1 = 1.2
            c2 = 1.2

            r1 = random.random()
            r2 = random.random()

            cząsteczka.prędkość = (
                w * cząsteczka.prędkość +
                c1 * r1 * (cząsteczka.najlepsza_pozycja - cząsteczka.pozycja) +
                c2 * r2 * (globalna_najlepsza_pozycja - cząsteczka.pozycja)
            )

            cząsteczka.pozycja += cząsteczka.prędkość

            wartość = Funkcja_próbna(cząsteczka.pozycja)

            if wartość < cząsteczka.najlepsza_wartość:
                cząsteczka.najlepsza_wartość = wartość
                cząsteczka.najlepsza_pozycja = cząsteczka.pozycja

            if wartość < globalna_najlepsza_wartość:
                globalna_najlepsza_wartość = wartość
                globalna_najlepsza_pozycja = cząsteczka.pozycja

    return globalna_najlepsza_pozycja, globalna_najlepsza_wartość

# Definicja funkcji testowej
def Funkcja_testowa(x):
    return np.sum(x ** 2, axis=0)

# Parametry
Rozmiar_Populacji = 50
MaxIteracje = 100
D = 2

# Uruchomienie algorytmu PSO dla jednej funkcji oceny
Wynik = "Uruchamianie Funkcji = Funkcja_testowa\n"
najlepsza_pozycja, najlepsza_wartość = PSO(Funkcja_testowa, Rozmiar_Populacji, D, MaxIteracje)
Wynik += "NAJLEPSZA POZYCJA: " + str(najlepsza_pozycja) + "\n"
Wynik += "NAJLEPSZA WARTOŚĆ: " + str(najlepsza_wartość) + "\n"
print(Wynik)

# Przygotowanie siatki punktów
x = np.linspace(-0.5, 0.5, 100)
y = np.linspace(-0.5, 0.5, 100)
x, y = np.meshgrid(x, y)
z = Funkcja_testowa(np.array([x, y]))

# Rysowanie wykresu
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, cmap='viridis')

# Punkt znaleziony przez minimalizację
najlepsza_pozycja, _ = PSO(Funkcja_testowa, 1, 2, 1)
ax.scatter(najlepsza_pozycja[0], najlepsza_pozycja[1], Funkcja_testowa(najlepsza_pozycja), color='red', s=100, label='Znaleziony punkt')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Wartość funkcji')

plt.title('Wykres funkcji testowej')
plt.show()


