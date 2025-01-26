import math

def euclidean_distance(xa, ya, xb, yb):
    return math.sqrt((xa - xb) ** 2 + (ya - yb) ** 2)

if __name__ == '__main__':
    print(euclidean_distance(35,35,0,0))