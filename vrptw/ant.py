class Ant:
    def __init__(self):
        self.routes = []
        self.vehicle = None

    def add_route(self, route):
        self.routes.append(route)

    def reset(self):
        self.routes = []
        if self.vehicle:
            self.vehicle.route = []
            self.vehicle.current_load = 0
            self.vehicle.current_time = 0
    
    def calculateDistanceSum(self):
        return sum([sum([customer.calculateDst(self.vehicle.route[i + 1]) for i, customer in enumerate(self.vehicle.route[:-1])]) for route in self.routes])

