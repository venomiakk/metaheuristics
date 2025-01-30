import matplotlib.pyplot as plt
from csvToPoints import csvToPoints


def plotPlainData(filename='data/r1type_vc200/R101.csv'):
    points = csvToPoints(filename)
    x = [point.xcord for point in points]
    y = [point.ycord for point in points]
    colors = ['ro' if point.custno != 1 else 'bo' for point in points]
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

if __name__ == '__main__':
    # plotPlainData()
    plotRoutes([[1, 2, 3, 4], [5, 6, 7, 8]], csvToPoints('data/r1type_vc200/R101.csv'))