import os
import cv2
from pathlib import Path

def wycinanie_i_zapisywanie_fragmentow(input_dir, output_dir, rozmiar_fragmentu):
    # Sprawdzenie czy katalog wyjściowy istnieje, jeśli nie, utwórz go
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Iteracja po plikach w katalogu wejściowym
    for plik in os.listdir(input_dir):
        sciezka_pliku = os.path.join(input_dir, plik)

        # Sprawdzenie czy ścieżka wskazuje na plik
        if not os.path.isfile(sciezka_pliku):
            continue

        # Wczytanie obrazu
        obraz = cv2.imread(sciezka_pliku)

        # Sprawdzenie czy obraz został poprawnie wczytany
        if obraz is not None:
            # Wycięcie fragmentów z obrazu
            for y in range(0, obraz.shape[0], rozmiar_fragmentu[1]):
                for x in range(0, obraz.shape[1], rozmiar_fragmentu[0]):
                    fragment = obraz[y:y+rozmiar_fragmentu[1], x:x+rozmiar_fragmentu[0]]

                    # Zapisanie wyciętego fragmentu do odpowiedniego katalogu
                    kategoria = os.path.splitext(plik)[0]  # Kategoria to nazwa pliku bez rozszerzenia
                    katalog_kategoria = os.path.join(output_dir, kategoria)
                    Path(katalog_kategoria).mkdir(parents=True, exist_ok=True)

                    nazwa_pliku_fragmentu = f"fragment_{y}_{x}_{plik}"
                    sciezka_wyjsciowa = os.path.join(katalog_kategoria, nazwa_pliku_fragmentu)
                    cv2.imwrite(sciezka_wyjsciowa, fragment)

# Ustawienia
katalog_wejsciowy = input("Podaj ścieżkę do katalogu wejściowego: ")
katalog_wyjsciowy = input("Podaj ścieżkę do katalogu wyjściowego: ")
rozmiar_fragmentu = (128, 128)

# Wywołanie funkcji do wycinania i zapisywania fragmentów
wycinanie_i_zapisywanie_fragmentow(katalog_wejsciowy, katalog_wyjsciowy, rozmiar_fragmentu)

print("Zakończono wycinanie i zapisywanie fragmentów.")
