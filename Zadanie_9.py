"""
Numer albumu: sXXXXX
Data: 2026-05-07
Prosty program do generowania sekwencji DNA i robienia na nich podstawowych operacji.
"""

import random

def validate_positive_int(tekst, min_v=1, max_v=100_000):
    """Pyta użytkownika o liczbę tak długo, aż poda poprawną."""
    while True:
        try:
            liczba = int(input(tekst))
            if min_v <= liczba <= max_v:
                return liczba
            print(f"Coś nie tak. Podaj liczbę od {min_v} do {max_v}.")
        except ValueError:
            print("To nie jest liczba! Spróbuj jeszcze raz.")

def generate_sequence(dlugosc):
    """Składa losowy ciąg liter ACGT o podanej długości."""
    nukleotydy = ['A', 'C', 'G', 'T']
    return "".join(random.choice(nukleotydy) for _ in range(dlugosc))

def calculate_stats(dna):
    """Liczy ile jest jakiego nukleotydu i zawartość GC."""
    ile = len(dna)
    wyniki = {}
    for n in "ACGT":
        procent = (dna.count(n) / ile) * 100
        wyniki[n] = round(procent, 2)
    
    # GC to suma G i C
    wyniki["GC"] = round(wyniki["G"] + wyniki["C"], 2)
    return wyniki

def insert_name(dna, imie):
    imie_male = imie.lower().replace(" ", "") # usuwamy spacje z imienia
    if len(dna) == 0:
        return imie_male
    miejsce = random.randint(0, len(dna))
    return dna[:miejsce] + imie_male + dna[miejsce:]

def format_fasta(id_seq, opis, sekwencja, szerokosc=80):
    """Robi z tekstu ładny format FASTA z łamaniem linii co 80 znaków."""
    naglowek = f">{id_seq} {opis}".strip()
    linie = [sekwencja[i:i+szerokosc] for i in range(0, len(sekwencja), szerokosc)]
    return naglowek + "\n" + "\n".join(linie)

# --- DODATKOWE FUNKCJE ---

def szukaj_motywu(dna, motyw):
    """Szuka gdzie w DNA chowa się podany kawałek tekstu."""
    pozycje = []
    szukany = motyw.upper()
    idx = dna.find(szukany)
    while idx != -1:
        pozycje.append(idx + 1) # +1 bo biolodzy liczą od 1
        idx = dna.find(szukany, idx + 1)
    return pozycje

def daj_komplementarna(dna, odwrotna=False):
    """Zamienia A na T, C na G itd. Opcjonalnie odwraca całość."""
    pary = str.maketrans("ACGT", "TGCA")
    nowe_dna = dna.translate(pary)
    if odwrotna:
        return nowe_dna[::-1]
    return nowe_dna

def zrob_rna(dna):
    """Zamienia T na U, czyli robi mRNA."""
    return dna.replace("T", "U")

def main():
    print("--- Generator Sekwencji DNA ---")
    
    # Pobieranie danych od usera
    ile_sztuk = validate_positive_int("Ile sekwencji wygenerować? ", 1, 10)
    dlugosc = validate_positive_int("Jak długa ma być sekwencja? ")
    
    moje_id = input("Podaj ID sekwencji (bez spacji!): ").strip()
    if " " in moje_id or not moje_id:
        moje_id = "Sekwencja_Testowa"
        
    moj_opis = input("Podaj jakiś opis (może być pusty): ")
    imie_usera = input("Podaj swoje imię: ")
    
    wszystkie_do_pliku = []
    
    # Główna pętla programu
    for nr in range(1, ile_sztuk + 1):
        aktualne_id = f"{moje_id}_{nr}"
        czyste_dna = generate_sequence(dlugosc)
        
        # Statystyki liczymy na czystym DNA (bez imienia)
        staty = calculate_stats(czyste_dna)
        
        # Do pliku idzie wersja z "wszytym" imieniem
        dna_z_imieniem = insert_name(czyste_dna, imie_usera)
        wszystkie_do_pliku.append(format_fasta(aktualne_id, moj_opis, dna_z_imieniem))
        
        # Dodatki: komplementarna i mRNA
        komp = daj_komplementarna(czyste_dna, odwrotna=True)
        wszystkie_do_pliku.append(format_fasta(f"{aktualne_id}_REV", "Nić odwrotna", komp))
        
        rna = zrob_rna(czyste_dna)
        wszystkie_do_pliku.append(format_fasta(f"{aktualne_id}_RNA", "Wersja mRNA", rna))
        
        # Wypisujemy info tylko dla pierwszej wygenerowanej sztuki
        if nr == 1:
            print(f"\nStatystyki dla pierwszej sekwencji ({aktualne_id}):")
            for k, v in staty.items():
                print(f"  {k}: {v}%")
            
            szukany = input("\nCzego szukamy w DNA? (np. ATG): ")
            trafienia = szukaj_motywu(czyste_dna, szukany)
            print(f"Znaleziono na pozycjach: {trafienia}")

    # Zapis wszystkiego do jednego pliku
    nazwa_pliku = f"{moje_id}.fasta"
    with open(nazwa_pliku, "w") as plik:
        plik.write("\n".join(wszystkie_do_pliku))
    
    print(f"\nZrobione! Wszystko jest w pliku {nazwa_pliku}")

if __name__ == "__main__":
    main()