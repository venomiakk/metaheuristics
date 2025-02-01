import matplotlib.pyplot as plt
from customer import Customer
from vehicle import Vehicle
from copy import deepcopy
import random

def csvToPoints(filename):
    points = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            fields = line.split(',')
            custno = int(fields[0]) - 1
            xcord = float(fields[1])
            ycord = float(fields[2])
            demand = float(fields[3])
            readytime = float(fields[4])
            duedate = float(fields[5])
            servicetime = float(fields[6])
            point = Customer(custno, xcord, ycord, demand, readytime, duedate, servicetime)
            points.append(point)
    return points

def getCustomersFromCSV(filename):
    points = csvToPoints(filename)
    depot = points.pop(0)
    return depot, points

def plotPlainData(filename='data/r1type_vc200/R101.csv'):
    points = csvToPoints(filename)
    x = [point.xcord for point in points]
    y = [point.ycord for point in points]
    colors = ['ro' if point.custno != 0 else 'bo' for point in points]
    for i in range(len(points)):
        plt.plot(x[i], y[i], colors[i])
    plt.show()

def plotRoutes(routes, points_dict, title='VRPTW Routes'):
    plt.figure(figsize=(8, 8))
    for idx, route in enumerate(routes):
        # `route` already contains Customer objects, so access coords directly
        x = [cust.xcord for cust in route]
        y = [cust.ycord for cust in route]
        plt.plot(x, y, marker='o', label=f'Route {idx+1}')
    plt.scatter(points_dict[0].xcord, points_dict[0].ycord, color='red', zorder=10, label='Depot')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(title)
    plt.legend()
    plt.show()

def greedy(depot, customers, capacity):
    unvisited = deepcopy(customers)
    vehicles = []
    # unvisited = [customer for customer in unvisited if customer not in test]
    # while len(unvisited) > 0:
    #     unvisited = unvisited[:int(len(unvisited)/2)]
    #     print(len(unvisited))
    while len(unvisited) > 0:
        vehicle = Vehicle(capacity, depot)
        vehicle.route.append(depot)
        possible_to_visit = unvisited.copy()
        
        while len(possible_to_visit) > 0:
            # 1. find nearest customer
            # nearest_customers = sorted(possible_to_visit, key=lambda x: vehicle.route[-1].calculateDst(x))[:5]
            random_number = random.uniform(0, 1)
            if random_number < 0.3:
                nearest_customer = min(possible_to_visit, key=lambda x: x.servicetime)
            else:
                nearest_customer = min(possible_to_visit, key=lambda x: vehicle.route[-1].calculateDst(x))

            possible_to_visit.remove(nearest_customer)
            # 2. check if can fit
            if not vehicle.canFit(nearest_customer):
                continue
            # 3. can make back to depot
            if not vehicle.canMakeBackToDepotFromCustomer(nearest_customer):
                continue
            # 4. can make it before due date
            if not vehicle.canVisitBeforeDueDate(nearest_customer):
                continue
            # 5. can visit in ready time or make it wait
            # 6. visit customer
            #? could take few customers in range and check min(readytime) and visit that customer
            if vehicle.canVisitInReadyTime(nearest_customer):
                vehicle.visit(nearest_customer)
            else:
                vehicle.waitForCustomer(nearest_customer)
                vehicle.visit(nearest_customer)
            # 7. remove customer from unvisited
            unvisited.remove(nearest_customer)
        
        vehicle.route.append(depot)
        vehicles.append(vehicle)
    
    return vehicles

def calculateSolutionDistance(vehicles):
    distance = 0
    for vehicle in vehicles:
        distance += vehicle.calculateRouteDistance()
    return distance


if __name__ == '__main__':
    points = csvToPoints('data/r1type_vc200/R101.csv')
    print(points[0])
    # plotPlainData()
    plotRoutes([[1, 2, 3, 4], [5, 6, 7, 8]], csvToPoints('data/r1type_vc200/R101.csv'))