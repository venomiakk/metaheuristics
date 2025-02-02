from v2.vehicle import Vehicle
from customer import Customer
from v2.utils import getCustomersFromCSV, csvToPoints, plotPlainData, plotRoutes, greedy, calculateSolutionDistance
from copy import deepcopy

# def ga_test():
#     file = 'data/c1type_vc200/C101.csv'
#     capacity = 200
#     allpoints = csvToPoints(file)
#     depot, customers = allpoints[0], allpoints[1:]
#     initial_solution = greedy(depot, customers, capacity)

#     best_solution, progress_history = optimize_vrptw(customers=customers, 
#                                    depot=depot, 
#                                    vehicle_capacity=capacity, 
#                                    initial_solution=initial_solution, 
#                                    )
#     print(progress_history)
#     print('Best Solution:')
#     print(best_solution)
#     best_routes = [vehicle.route for vehicle in best_solution]
#     initial_routes = [vehicle.route for vehicle in initial_solution]
#     plotRoutes(best_routes, allpoints, f'Best Solution, nV: {len(best_routes)}')
#     plotRoutes(initial_routes, allpoints, f'Initial Solution, nV: {len(initial_routes)}')


def main():
    file = 'data/c1type_vc200/C101.csv'
    capacity = 200
    allpoints = csvToPoints(file)
    depot, customers = allpoints[0], allpoints[1:]
    vehicles = greedy(depot, customers, capacity)
    distance = 0
    for idx, vehicle in enumerate(vehicles):
        r_dst = vehicle.calculateRouteDistance()
        distance += r_dst
        rt = vehicle.routeToString()
        print(f'Route {idx+1}: {rt}, Distance: {r_dst}, Time: {vehicle.current_time}, Load: {vehicle.current_load}')

    print(f'Dst: {distance}, Vehicles: {len(vehicles)}')
    routes = [vehicle.route for vehicle in vehicles]
    plotRoutes(routes, allpoints)
    # plotPlainData(file)


if __name__ == '__main__':
   main()