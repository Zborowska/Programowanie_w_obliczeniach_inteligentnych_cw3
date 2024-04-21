import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

def pobierz_sciezki_plikow():
    sciezki_plikow = []
    for i in range(3):
        sciezka = input("Podaj ścieżkę do pliku CSV {}: ".format(i+1))
        sciezki_plikow.append(sciezka)
    return sciezki_plikow

# Pobranie ścieżek do trzech plików CSV
sciezki_plikow = pobierz_sciezki_plikow()

# Wczytanie danych z trzech plików CSV
ramki_danych = []
for sciezka in sciezki_plikow:
    ramka_danych = pd.read_csv(sciezka)
    ramki_danych.append(ramka_danych)

# Połączenie danych z trzech plików CSV w jeden DataFrame
dane = pd.concat(ramki_danych, ignore_index=True)

# Podział danych na cechy (X) i etykiety (y)
X = dane.drop('Category', axis=1)  # Usunięcie kolumny z etykietami
y = dane['Category']

# Podział danych na zbiory treningowy i testowy
X_treningowe, X_testowe, y_treningowe, y_testowe = train_test_split(X, y, test_size=0.2, random_state=42)

# Utworzenie klasyfikatora SVM
klasyfikator_svm = SVC(kernel='linear', random_state=42)

# Uczenie klasyfikatora na zbiorze treningowym
klasyfikator_svm.fit(X_treningowe, y_treningowe)

# Klasyfikacja danych testowych
y_pred = klasyfikator_svm.predict(X_testowe)

# Obliczenie dokładności klasyfikatora
dokladnosc = accuracy_score(y_testowe, y_pred)

# Wyświetlenie dokładności klasyfikatora
print("Dokładność klasyfikatora SVM:", dokladnosc)
