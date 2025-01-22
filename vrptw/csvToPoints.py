from customer import Customer

def csvToPoints(filename):
    points = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            fields = line.split(',')
            custno = int(fields[0])
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

if __name__ == '__main__':
    points = csvToPoints('data/r1type_vc200/R101.csv')
    print(points[0].calculateDst(points[1]))
    print(points[1].calculateDst(points[0]))