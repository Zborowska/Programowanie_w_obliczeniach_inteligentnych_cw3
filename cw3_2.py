import os
import numpy as np
import pandas as pd
import mahotas as mh
from skimage import io, color


# Funkcja do obliczania cech tekstury dla jednej próbki tekstury
def oblicz_cechy_tekstury(obraz, odleglosci):
    # Przekształcenie obrazu na skalę szarości
    obraz_szary = color.rgb2gray(obraz)

    # Zmniejszenie głębi jasności do 5 bitów (64 poziomy)
    obraz_szary = (obraz_szary * 63).astype(np.uint8)

    # Inicjalizacja listy cech
    cechy = []

    # Obliczanie macierzy zdarzeń dla każdej odległości
    for odleglosc in odleglosci:
        glcm = mh.features.haralick(obraz_szary, distance=odleglosc)
        # Obliczanie cech tekstury
        dissimilarity = np.mean(glcm[..., 1])  # Średnia wartość dla dysymetrii
        correlation = np.mean(glcm[..., 2])  # Średnia wartość dla korelacji
        contrast = np.mean(glcm[..., 4])  # Średnia wartość dla kontrastu
        energy = np.mean(glcm[..., 8])  # Średnia wartość dla energii
        homogeneity = np.mean(glcm[..., 7])  # Średnia wartość dla jednorodności
        ASM = np.mean(glcm[..., 0])  # Średnia wartość dla ASM
        # Dodanie cech do listy
        cechy.extend([dissimilarity, correlation, contrast, energy, homogeneity, ASM])

    return cechy

# Funkcja do wczytywania próbek tekstury z folderu i obliczania cech dla każdej próbki
def przetworz_próbki_tekstury(sciezka_folderu, odleglosci, kąty):
    # Inicjalizacja listy cech i kategorii tekstur
    lista_cech = []
    kategorie = []

    # Przetwarzanie każdej próbki tekstury
    for nazwa_pliku in os.listdir(sciezka_folderu):
        # Sprawdzenie, czy plik jest plikiem obrazu
        if nazwa_pliku.endswith(('.jpg', '.jpeg', '.png')):
            # Wczytanie obrazu
            obraz = io.imread(os.path.join(sciezka_folderu, nazwa_pliku))
            # Obliczanie cech tekstury
            cechy = oblicz_cechy_tekstury(obraz, odleglosci)
            # Dodawanie cech do listy
            lista_cech.append(cechy)
            # Dodawanie nazwy pliku jako kategorii tekstury
            kategoria = nazwa_pliku.split('.')[0]  # Zakładam, że nazwa pliku bez rozszerzenia to nazwa kategorii
            kategorie.append(kategoria)

    return lista_cech, kategorie


# Lista ścieżek do folderów z próbkami tekstury
sciezki_folderow = [
    r"C:\Users\Paulina\Documents\sciezka_cw3\wyj\IMG_5927",
    r"C:\Users\Paulina\Documents\sciezka_cw3\wyj\IMG_5927",
    r"C:\Users\Paulina\Documents\sciezka_cw3\wyj\IMG_5927"
]

# Odległości pikseli
odleglosci = [1, 3, 5]

# Kąty
kąty = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]

# Przetwarzanie każdego z folderów
for i, sciezka_folderu in enumerate(sciezki_folderow):
    # Obliczanie cech tekstury dla próbek w folderze
    lista_cech, kategorie = przetworz_próbki_tekstury(sciezka_folderu, odleglosci, kąty)

    # Tworzenie DataFrame z cechami i kategoriami tekstur
    nazwy_kolumn = ['dissimilarity', 'correlation', 'contrast', 'energy', 'homogeneity', 'ASM'] * len(odleglosci)
    df = pd.DataFrame(lista_cech, columns=nazwy_kolumn)
    df['Kategoria'] = kategorie

    # Zapisywanie danych do pliku CSV
    plik_wyjsciowy = f'cechy_tekstury_{i + 1}.csv'
    df.to_csv(plik_wyjsciowy, index=False)



