from vehicle import Vehicle
from customer import Customer
from csvToPoints import getCustomersFromCSV, csvToPoints
from copy import deepcopy
from plots import plotPlainData, plotRoutes
from ga import optimize_vrptw

def greedyByTime(depot, customers, capacity):
    unvisited = deepcopy(customers)
    vehicles = []
    unvisited = sorted(unvisited, key=lambda x: x.duedate)
    while len(unvisited) > 0:
        vehicle = Vehicle(capacity, depot)
        vehicle.route.append(depot)
        
        for customer in unvisited:
            if vehicle.canVisit(customer):
                vehicle.visit(customer)
                unvisited.remove(customer)
            elif vehicle.canFit(customer):
                vehicle.waitForCustomer(customer)
                vehicle.visit(customer)
                unvisited.remove(customer)

        vehicle.route.append(depot)
        vehicles.append(vehicle)
    return vehicles

def greedyByDistance(depot, customers, capacity):
    unvisited = deepcopy(customers)
    for customer in unvisited:
        customer.setDstToDepot(depot)
        
    vehicles = []
    unvisited = sorted(unvisited, key=lambda x: x.dsttodepot)
    while len(unvisited) > 0:
        vehicle = Vehicle(capacity, depot)
        vehicle.route.append(depot)
        
        for customer in unvisited:
            if vehicle.canVisit(customer):
                vehicle.visit(customer)
                unvisited.remove(customer)
            elif vehicle.canFit(customer):
                vehicle.waitForCustomer(customer)
                vehicle.visit(customer)
                unvisited.remove(customer)

        vehicle.route.append(depot)
        vehicles.append(vehicle)
    return vehicles

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

def test1():
    file = 'data/c1type_vc200/C101.csv'
    capacity = 200
    # plotPlainData(file)
    allpoints = csvToPoints(file)
    depot, customers = allpoints[0], allpoints[1:]

    print('Greedy by Time')
    vehicles = greedyByTime(depot, customers, capacity)
    for vehicle in vehicles:
        print(vehicle.printRoute())
    routes = [vehicle.route for vehicle in vehicles]
    plotRoutes(routes, allpoints, 'Greedy by Time')

    print('Greedy by Distance')
    vehicles = greedyByDistance(depot, customers, capacity)
    for vehicle in vehicles:
        print(vehicle.printRoute())
    routes = [vehicle.route for vehicle in vehicles]
    plotRoutes(routes, allpoints, 'Greedy by Distance')

def test2():
    file = 'data/r1type_vc200/R101.csv'
    capacity = 200
    allpoints = csvToPoints(file)
    depot, customers = allpoints[0], allpoints[1:]
    vehicles = greedy(depot, customers, capacity)
    distance = 0
    for idx, vehicle in enumerate(vehicles):
        distance += vehicle.calculateRouteDistance()
        rt = vehicle.routeToString()
        print(f'Route {idx+1}: {rt}')

    print(f'Dst: {distance}, Vehicles: {len(vehicles)}')
    routes = [vehicle.route for vehicle in vehicles]
    plotRoutes(routes, allpoints)
    

def main():
    file = 'data/r1type_vc200/R101.csv'
    capacity = 200
    allpoints = csvToPoints(file)
    depot, customers = allpoints[0], allpoints[1:]
    initial_solution = greedy(depot, customers, capacity)

    best_solution = optimize_vrptw(customers=customers, 
                                   depot=depot, 
                                   vehicle_capacity=capacity, 
                                   initial_solution=initial_solution, 
                                   )
    print('Best Solution:')
    print(best_solution)

if __name__ == '__main__':
    main()