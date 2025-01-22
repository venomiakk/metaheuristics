import matplotlib.pyplot as plt
from csvToPoints import csvToPoints


def plotPlainData():
    points = csvToPoints('data/r1type_vc200/R101.csv')
    x = [point.xcord for point in points]
    y = [point.ycord for point in points]
    colors = ['ro' if point.custno != 1 else 'bo' for point in points]
    for i in range(len(points)):
        plt.plot(x[i], y[i], colors[i])
    plt.show()

if __name__ == '__main__':
    plotPlainData()