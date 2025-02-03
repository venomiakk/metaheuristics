import csv
from customer import Customer
import math

def load_data(file_path):
    customers = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            id = int(row[0])
            x = float(row[1])
            y = float(row[2])
            demand = float(row[3])
            ready_time = float(row[4])
            due_date = float(row[5])
            service_time = float(row[6])
            customers.append(Customer(id, x, y, demand, ready_time, due_date, service_time))
    depot = customers[0]
    customers = customers[1:]
    return depot, customers

def euclidean_distance(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

def time_feasible_route(route, depot, distance_matrix):
    current_time = 0
    prev = depot
    for customer in route:
        arrival = current_time + distance_matrix[prev.id][customer.id]
        arrival = max(arrival, customer.ready_time)
        if arrival > customer.due_date:
            return False
        departure = arrival + customer.service_time
        current_time = departure
        prev = customer
    return True

def time_feasible(route, customer, position, depot, distance_matrix):
    current_time = 0
    current_load = 0
    prev = depot
    for i in range(len(route) + 1):
        if i == position:
            arrival = current_time + distance_matrix[prev.id][customer.id]
            arrival = max(arrival, customer.ready_time)
            departure = arrival + customer.service_time
            if arrival > customer.due_date:
                return False
            current_time = departure
            prev = customer
        if i < len(route):
            next_c = route[i]
            arrival = current_time + distance_matrix[prev.id][next_c.id]
            arrival = max(arrival, next_c.ready_time)
            if arrival > next_c.due_date:
                return False
            departure = arrival + next_c.service_time
            current_time = departure
            prev = next_c
    return True

def route_capacity_feasible(route, vehicle_capacity):
    total_demand = sum(c.demand for c in route)
    return total_demand <= vehicle_capacity

def capacity_feasible(route, customer, vehicle_capacity):
    total_demand = sum(c.demand for c in route) + customer.demand
    return total_demand <= vehicle_capacity

# SA
def calculate_route_distance(route, depot, distance_matrix):
    if not route:
        return 0
    total = distance_matrix[depot.id][route[0].id]
    for i in range(len(route)-1):
        total += distance_matrix[route[i].id][route[i+1].id]
    total += distance_matrix[route[-1].id][depot.id]
    return total

def calculate_objective(routes, depot, distance_matrix):
    num_vehicles = len(routes)
    total_distance = sum(calculate_route_distance(route, depot, distance_matrix) for route in routes)
    return num_vehicles * 1e6 + total_distance