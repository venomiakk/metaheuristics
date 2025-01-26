import requests
from bs4 import BeautifulSoup
import csv

# URL strony
url = "http://web.cba.neu.edu/~msolomon/rc201.htm"

# Pobranie zawartości strony
response = requests.get(url)
response.raise_for_status()

# Parsowanie HTML
soup = BeautifulSoup(response.text, 'html.parser')


# albo 'b' albo 'p'
tt_tags = soup.find_all('b')
# Dane z tabel
tables = {}  # Słownik: klucze - nagłówki (R101, R102), wartości - dane tabeli

current_header = None

for tt in tt_tags:
    # Szukanie tagów <font>
    font_tags = tt.find_all('font')
    for font in font_tags:
        # Pobranie tekstu i czyszczenie
        raw_text = font.get_text(strip=True)
        clean_text = ' '.join(raw_text.replace('\xa0', ' ').split())
        
        # Jeśli to nagłówek tabeli (np. R101)
        if clean_text.startswith("RC2"):
            current_header = clean_text
            tables[current_header] = []  # Inicjalizacja tabelki
        else:
            # Jeśli są dane, dodaj je do aktualnej tabeli
            if current_header:
                # Usuwanie wiersza z nagłówkiem kolumn
                if not clean_text.lower().startswith(("cust no", "xcoord", "ready timer", "due date")):
                    tables[current_header].append(clean_text.split())

# Zapisanie każdej tabeli do pliku CSV
for header, data in tables.items():
    filename = f"{header}.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Dodaj dane do pliku CSV
        for row in data:
            writer.writerow(row)
    
    print(f"Tabelka {header} zapisana do pliku {filename}.")

print("Wszystkie tabelki zostały zapisane w formacie CSV.")
