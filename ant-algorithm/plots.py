import matplotlib.pyplot as plt

# Wczytanie danych z pliku
file_path = 'data/A-n32-k5.txt'
data = []

with open(file_path, 'r') as file:
    for line in file:
        parts = line.split()
        index = int(parts[0])
        x = int(parts[1])
        y = int(parts[2])
        data.append((index, x, y))

# Rozdzielenie danych na listy x i y
indices, x_coords, y_coords = zip(*data)

# Tworzenie wykresu
plt.scatter(x_coords, y_coords)

# Dodanie etykiet do punktów
for i, txt in enumerate(indices):
    plt.annotate(txt, (x_coords[i], y_coords[i]))

# Dodanie tytułu i etykiet osi
plt.title('Wykres punktowy z pliku A-n32-k5.txt')
plt.xlabel('Współrzędna X')
plt.ylabel('Współrzędna Y')

# Wyświetlenie wykresu
plt.show()