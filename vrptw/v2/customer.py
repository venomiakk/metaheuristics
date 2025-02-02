class Customer:
    def __init__(self, custno, xcord, ycord, demand, readytime, duedate, servicetime):
        self.custno = custno
        self.xcord = xcord
        self.ycord = ycord
        self.demand = demand
        self.readytime = readytime
        self.duedate = duedate
        self.servicetime = servicetime
        self.visited = False
        self.dsttodepot = None

    def setDstToDepot(self, depot):
        self.dsttodepot = ((self.xcord - depot.xcord)**2 + (self.ycord - depot.ycord)**2)**0.5

    def __str__(self):
        return f"Customer:{self.custno} {self.xcord}, {self.ycord}, {self.demand}, {self.readytime}, {self.duedate}, {self.servicetime}"
    
    def calculateDst(self, other):
        return ((self.xcord - other.xcord)**2 + (self.ycord - other.ycord)**2)**0.5