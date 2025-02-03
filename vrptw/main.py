from outputdata import save_results, plot_routes, save_results_csv, plot_results, save_results_txt
from sa import run_sa, calculate_route_distance

#best so far 
# cooling_rate = 0.950
G_ITERS = 10000
G_CR = 0.950
G_INITTEMP = 10000

def test1():
    filepath = 'data/rc1type_vc200/RC101.csv'
    vcapacity = 200
    test_file='RC101'
    path = 'test1'
    best_Dst = 1696.94
    best_Vehicles = 14
    init_temp = G_INITTEMP
    cooling_rate = G_CR
    iterations = G_ITERS
    csvdata = []
    for i in range(10):
        row = []
        row.append(i)
        initial_routes, optimized_routes, depot, distance_matrix = run_sa(filepath=filepath, vehicle_capacity=vcapacity, 
                                                                          initial_temp=init_temp, cooling_rate=cooling_rate, 
                                                                          iterations=iterations)
        total_dst = 0
        total_vehicles = len(optimized_routes)
        for r in optimized_routes:
            total_dst += calculate_route_distance(r, depot, distance_matrix)
        row.append(total_vehicles)
        row.append(total_dst)
        csvdata.append(row)
        plot_routes(optimized_routes, depot, filename=f'{path}/routes_{i}.png', 
                    initial_temp=init_temp, cooling_rate=cooling_rate, iterations=iterations,
                      data_file=test_file, dst=total_dst)
    save_results_txt(csvdata, f'{path}/results.txt', iterations=iterations, initial_temp=init_temp, 
                     cooling_rate=cooling_rate, instance_name=test_file)
    save_results_csv(csvdata, f'{path}/results.csv')
    plot_results(data=csvdata, filename=f'{path}/results.png', best_distance=best_Dst, best_vehicles=best_Vehicles,
                  iterations=iterations, cooling_rate=cooling_rate, initial_temp=init_temp, data_file=test_file)

def test2():
    filepath = 'data/rc1type_vc200/RC101.csv'
    vcapacity = 200
    test_file='RC101'
    path = 'test2'
    best_Dst = 1696.94
    best_Vehicles = 14
    init_temp = 10000
    cooling_rate = G_CR
    iterations = G_ITERS
    csvdata = []
    for i in range(10):
        row = []
        row.append(i)
        initial_routes, optimized_routes, depot, distance_matrix = run_sa(filepath=filepath, vehicle_capacity=vcapacity, 
                                                                          initial_temp=init_temp, cooling_rate=cooling_rate, 
                                                                          iterations=iterations)
        total_dst = 0
        total_vehicles = len(optimized_routes)
        for r in optimized_routes:
            total_dst += calculate_route_distance(r, depot, distance_matrix)
        row.append(total_vehicles)
        row.append(total_dst)
        csvdata.append(row)
        plot_routes(optimized_routes, depot, filename=f'{path}/routes_{i}.png', 
                    initial_temp=init_temp, cooling_rate=cooling_rate, iterations=iterations,
                      data_file=test_file, dst=total_dst)
    save_results_txt(csvdata, f'{path}/results.txt', iterations=iterations, initial_temp=init_temp, 
                     cooling_rate=cooling_rate, instance_name=test_file)
    save_results_csv(csvdata, f'{path}/results.csv')
    plot_results(data=csvdata, filename=f'{path}/results.png', best_distance=best_Dst, best_vehicles=best_Vehicles,
                  iterations=iterations, cooling_rate=cooling_rate, initial_temp=init_temp, data_file=test_file)

def test3():
    filepath = 'data/c1type_vc200/C101.csv'
    vcapacity = 200
    test_file='C101'
    path = 'test3'
    best_Dst = 828.94
    best_Vehicles = 10
    init_temp = 100000
    cooling_rate = G_CR
    iterations = G_ITERS
    csvdata = []
    for i in range(10):
        row = []
        row.append(i)
        initial_routes, optimized_routes, depot, distance_matrix = run_sa(filepath=filepath, vehicle_capacity=vcapacity, 
                                                                          initial_temp=init_temp, cooling_rate=cooling_rate, 
                                                                          iterations=iterations)
        total_dst = 0
        total_vehicles = len(optimized_routes)
        for r in optimized_routes:
            total_dst += calculate_route_distance(r, depot, distance_matrix)
        row.append(total_vehicles)
        row.append(total_dst)
        csvdata.append(row)
        plot_routes(optimized_routes, depot, filename=f'{path}/routes_{i}.png', 
                    initial_temp=init_temp, cooling_rate=cooling_rate, iterations=iterations,
                      data_file=test_file, dst=total_dst)
    save_results_txt(csvdata, f'{path}/results.txt', iterations=iterations, initial_temp=init_temp, 
                     cooling_rate=cooling_rate, instance_name=test_file)
    save_results_csv(csvdata, f'{path}/results.csv')
    plot_results(data=csvdata, filename=f'{path}/results.png', best_distance=best_Dst, best_vehicles=best_Vehicles,
                  iterations=iterations, cooling_rate=cooling_rate, initial_temp=init_temp, data_file=test_file)

def run_first():
    # Run simulated annealing
    initial_routes, optimized_routes, depot, distance_matrix = run_sa(filepath='data/rc1type_vc200/RC101.csv',
                                                                       vehicle_capacity=200, initial_temp=1000, 
                                                                       cooling_rate=0.995, iterations=10000)

    save_results(initial_routes, depot, distance_matrix, "initial_results.txt")
    plot_routes(initial_routes, depot, "initial_routes.png")

    save_results(optimized_routes, depot, distance_matrix, "optimized_results.txt")
    plot_routes(optimized_routes, depot, "optimized_routes.png")
    
    # # Terminal output
    print("\nResults saved to:")
    print("- output/initial_results.txt")
    print("- output/initial_routes.png")
    print("- output/optimized_results.txt")
    print("- output/optimized_routes.png")


def run_c101():
    filepath = 'data/c1type_vc200/C101.csv'
    vcapacity = 200
    test_file='C101'
    path = 'c101'
    best_Dst = 828.94
    best_Vehicles = 10
    init_temp = 100000
    cooling_rate = G_CR
    iterations = G_ITERS
    csvdata = []
    for i in range(10):
        row = []
        row.append(i)
        initial_routes, optimized_routes, depot, distance_matrix = run_sa(filepath=filepath, vehicle_capacity=vcapacity, 
                                                                          initial_temp=init_temp, cooling_rate=cooling_rate, 
                                                                          iterations=iterations)
        total_dst = 0
        total_vehicles = len(optimized_routes)
        for r in optimized_routes:
            total_dst += calculate_route_distance(r, depot, distance_matrix)
        row.append(total_vehicles)
        row.append(total_dst)
        csvdata.append(row)
        plot_routes(optimized_routes, depot, filename=f'{path}/routes_{i}.png', 
                    initial_temp=init_temp, cooling_rate=cooling_rate, iterations=iterations,
                      data_file=test_file, dst=total_dst)
    save_results_txt(csvdata, f'{path}/results.txt', iterations=iterations, initial_temp=init_temp, 
                     cooling_rate=cooling_rate, instance_name=test_file)
    save_results_csv(csvdata, f'{path}/results.csv')
    plot_results(data=csvdata, filename=f'{path}/results.png', best_distance=best_Dst, best_vehicles=best_Vehicles,
                  iterations=iterations, cooling_rate=cooling_rate, initial_temp=init_temp, data_file=test_file)

def run_r101():
    filepath = 'data/r1type_vc200/r101.csv'
    vcapacity = 200
    test_file='R101'
    path = 'r101'
    best_Dst = 1645.79
    best_Vehicles = 19
    init_temp = 100000
    cooling_rate = G_CR
    iterations = G_ITERS
    csvdata = []
    for i in range(10):
        row = []
        row.append(i)
        initial_routes, optimized_routes, depot, distance_matrix = run_sa(filepath=filepath, vehicle_capacity=vcapacity, 
                                                                          initial_temp=init_temp, cooling_rate=cooling_rate, 
                                                                          iterations=iterations)
        total_dst = 0
        total_vehicles = len(optimized_routes)
        for r in optimized_routes:
            total_dst += calculate_route_distance(r, depot, distance_matrix)
        row.append(total_vehicles)
        row.append(total_dst)
        csvdata.append(row)
        plot_routes(optimized_routes, depot, filename=f'{path}/routes_{i}.png', 
                    initial_temp=init_temp, cooling_rate=cooling_rate, iterations=iterations,
                      data_file=test_file, dst=total_dst)
    save_results_txt(csvdata, f'{path}/results.txt', iterations=iterations, initial_temp=init_temp, 
                     cooling_rate=cooling_rate, instance_name=test_file)
    save_results_csv(csvdata, f'{path}/results.csv')
    plot_results(data=csvdata, filename=f'{path}/results.png', best_distance=best_Dst, best_vehicles=best_Vehicles,
                  iterations=iterations, cooling_rate=cooling_rate, initial_temp=init_temp, data_file=test_file)


def run_rc101():
    filepath = 'data/rc1type_vc200/rc101.csv'
    vcapacity = 200
    test_file='RC101'
    path = 'rc101'
    best_Dst = 1696.94
    best_Vehicles = 14
    init_temp = 100000
    cooling_rate = G_CR
    iterations = G_ITERS
    csvdata = []
    for i in range(10):
        row = []
        row.append(i)
        initial_routes, optimized_routes, depot, distance_matrix = run_sa(filepath=filepath, vehicle_capacity=vcapacity, 
                                                                          initial_temp=init_temp, cooling_rate=cooling_rate, 
                                                                          iterations=iterations)
        total_dst = 0
        total_vehicles = len(optimized_routes)
        for r in optimized_routes:
            total_dst += calculate_route_distance(r, depot, distance_matrix)
        row.append(total_vehicles)
        row.append(total_dst)
        csvdata.append(row)
        plot_routes(optimized_routes, depot, filename=f'{path}/routes_{i}.png', 
                    initial_temp=init_temp, cooling_rate=cooling_rate, iterations=iterations,
                      data_file=test_file, dst=total_dst)
    save_results_txt(csvdata, f'{path}/results.txt', iterations=iterations, initial_temp=init_temp, 
                     cooling_rate=cooling_rate, instance_name=test_file)
    save_results_csv(csvdata, f'{path}/results.csv')
    plot_results(data=csvdata, filename=f'{path}/results.png', best_distance=best_Dst, best_vehicles=best_Vehicles,
                  iterations=iterations, cooling_rate=cooling_rate, initial_temp=init_temp, data_file=test_file)

def main():
    run_c101()
    run_r101()
    run_rc101()
    

if __name__ == '__main__':
    main()