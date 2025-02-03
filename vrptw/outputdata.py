import os
import matplotlib.pyplot as plt
from sa import calculate_route_distance
import csv
import numpy as np
import math

def plot_routes(routes, depot, filename="routes.png", data_file=None, iterations=None, cooling_rate=None, initial_temp=None, dst=0):
    plt.figure(figsize=(10, 10))
    
    plt.scatter(depot.x, depot.y, c='red', s=100, marker='s', edgecolors='black', label='Magazyn', zorder=10)
    
    colors = plt.cm.tab20.colors
    for i, route in enumerate(routes):
        if not route:
            continue

        x = [depot.x] + [c.x for c in route] + [depot.x]
        y = [depot.y] + [c.y for c in route] + [depot.y]
        
        plt.scatter(
            [c.x for c in route], 
            [c.y for c in route], 
            color=colors[i % 20],
            s=50,
            label=f'Pojazd {i+1}' if i < 20 else None
        )
        
        plt.plot(x, y, linestyle='-', linewidth=1, color=colors[i % 20])
    
    title = f"{data_file}, Iteracje: {iterations}, Początkowa temperatura: {initial_temp}, Wsp. schładzania: {cooling_rate}, Odległość: {dst:.2f}"
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    os.makedirs("output", exist_ok=True)
    plt.savefig(f"output/{filename}")
    plt.close()

def save_results(routes, depot, distance_matrix, filename="results.txt"):
    os.makedirs("output", exist_ok=True)
    with open(f"output/{filename}", "w") as f:
        total_distance = 0
        total_vehicles = len(routes)
        
        f.write("Trasy:\n")
        f.write("="*50 + "\n")
        
        for i, route in enumerate(routes):
            route_distance = calculate_route_distance(route, depot, distance_matrix)
            total_distance += route_distance
            
            route_ids = [depot.id] + [c.id for c in route] + [depot.id]
            
            f.write(f"Trasa {i+1}:\n")
            f.write(f"  Klienci: {len(route)}\n")
            f.write(f"  Kolejność: {route_ids}\n")
            f.write(f"  Odległość: {route_distance:.2f}\n")
            f.write("-"*50 + "\n")
        
        f.write("\nSummary:\n")
        f.write("="*50 + "\n")
        f.write(f"Total Vehicles: {total_vehicles}\n")
        f.write(f"Total Distance: {total_distance:.2f}\n")


def save_results_csv(data, filename="results.txt"):
    os.makedirs("output", exist_ok=True)
    with open(f"output/{filename}", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Iteration', 'Vehicles', 'Distance'])
        writer.writerows(data)

def save_results_txt(data, filename="results.txt",
                    iterations=None, initial_temp=None, cooling_rate=None, instance_name=None):
    
    dst = [d[2] for d in data]
    nv = [d[1] for d in data]
    title = f'{instance_name}, Iteracje: {iterations}, Poczatkowa temperatura: {initial_temp}, Wsp. schladzania: {cooling_rate}'
    os.makedirs("output", exist_ok=True)
    with open(f"output/{filename}", "a") as f:
        f.write(f'{title}\n')
        f.write('Pojazdy, Odleglosc\n')
        for i in range(len(dst)):
            f.write(f'{nv[i]}, {dst[i]}\n')
        f.write('\n')
        f.write('Najlepsze\n')
        f.write(f'{np.round(min(dst),2)}, {min(nv)}\n')
        f.write('Srednie\n')
        f.write(f'{np.round(sum(dst)/len(dst),2)}, {sum(nv)/len(nv)}\n')
        f.write('Najgorsze\n')
        f.write(f'{np.round(max(dst),2)}, {max(nv)}\n')
        f.write('\n')
        f.write("\n" + "="*50 + "\n\n")
        

def plot_results(data, best_distance=None, best_vehicles=None, filename="combined_results.png", iterations=None, cooling_rate=None, initial_temp=None, data_file=None):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    fig.suptitle(f'{data_file}, Iteracje: {iterations}, Początkowa temperatura: {initial_temp}, Wsp. schładzania: {cooling_rate}', fontsize=16, y=0.98)
    x_values = [d[0] for d in data]
    distances = [d[2] for d in data]
    vehicles = [d[1] for d in data]
    
    min_dst = min(distances)
    if best_distance:
        min_dst = min(min_dst, best_distance)
    max_dst = max(distances)
    if best_distance:
        max_dst = max(max_dst, best_distance)
    min_dst = math.floor(min_dst / 100) * 100
    max_dst = math.ceil(max_dst / 100) * 100
    
    max_vehicles = max(vehicles)
    max_vehicles = max(max_vehicles, best_vehicles) if best_vehicles else max_vehicles
    min_vehicles = min(vehicles)
    min_vehicles = min(min_vehicles, best_vehicles) if best_vehicles else min_vehicles
    
    # Distance plot
    ax1.plot(x_values, distances, linestyle='-', marker='o', color='blue', label='Uzyskane wyniki')
    ax1.set_xticks(range(min(x_values), max(x_values) + 1))
    y_range = np.arange(start=int(min_dst)-100, 
                       stop=int(max_dst)+200, 
                       step=100)
    ax1.set_yticks(y_range)
    
    for x, y in zip(x_values, distances):
        ax1.annotate(f'{y:.0f}', (x, y), xytext=(0, 10), textcoords='offset points', ha='center')
    if best_distance:
        ax1.axhline(y=best_distance, color='red', linestyle='--', label='Najlepsza odległość')
    ax1.set_title("Odległość w kolejnych uruchomieniach")
    ax1.set_xlabel("Uruchomienia")
    ax1.set_ylabel("Odległość")
    ax1.grid(True)
    ax1.legend()
    
    ax2.plot(x_values, vehicles, linestyle='-', marker='o', color='green', label='Uzyskane wyniki')
    ax2.set_xticks(range(min(x_values), max(x_values) + 1))
    ax2.set_yticks(range(int(min_vehicles) - 2, int(max_vehicles) + 3))
    
    for x, y in zip(x_values, vehicles):
        ax2.annotate(f'{y}', (x, y), xytext=(0, 10), textcoords='offset points', ha='center')
    if best_vehicles:
        ax2.axhline(y=best_vehicles, color='red', linestyle='--', label='Najlepsza liczba pojazdów')
    ax2.set_title("Liczba pojazdów w kolejnych uruchomieniach")
    ax2.set_xlabel("Uruchomienia")
    ax2.set_ylabel("Liczba pojazdów")
    ax2.grid(True)
    ax2.legend()
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.9) 
    os.makedirs("output", exist_ok=True)
    plt.savefig(f"output/{filename}")
    plt.close()