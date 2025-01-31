from typing import List
from customer import Customer


# Vehicle class with speed attribute
class Vehicle:
    def __init__(self, capacity, depot, speed=50):
        self.capacity = capacity
        self.route: List[Customer] = []
        self.speed = speed / 10 #! need to experiment with this
        self.depot = depot
        self.max_time = self.depot.duedate
        self.current_load = 0
        self.current_time = 0

    def calculateRouteDistance(self):
        distance = 0
        for i in range(1, len(self.route)):
            distance += self.route[i-1].calculateDst(self.route[i])
        return distance

    def calculateDistance(self, next_customer):
        return self.route[-1].calculateDst(next_customer)

    def calculateArrivalTime(self, customer):
        dst = self.route[-1].calculateDst(customer)
        return (float(dst) / float(self.speed)) + float(self.current_time)

    def calculateTimeToNextCustomer(self, customer):
        dst = self.route[-1].calculateDst(customer)
        return float(dst) / float(self.speed)

    def calculateArrivalTimeFromPointToPoint(self, location1, location2):
        dst = location1.calculateDst(location2)
        return (float(dst) / float(self.speed)) + float(self.current_time)
    
    def calculateArrivalTimeToDepot(self, location):
        dst = location.calculateDst(self.depot)
        return (float(dst) / float(self.speed)) + float(self.current_time)
    
    # TODO Check if this is correct
    def canVisit(self, customer):
        if self.current_load + customer.demand > self.capacity:
            # print('Capacity')
            return False
        if self.calculateArrivalTime(customer) > customer.duedate:
            # print('Due Date')
            return False
        if self.calculateArrivalTime(customer) < customer.readytime:
            # print('Ready Time')
            return False
        if self.calculateArrivalTime(customer) + customer.servicetime + self.calculateArrivalTimeToDepot(customer) > self.max_time:
            # print('Service Time')
            return False
        return True
    
    def canVisitInReadyTime(self, customer):
        if self.calculateArrivalTime(customer) < customer.readytime:
            # print('Ready Time')
            return False
        return True
    
    def canVisitBeforeDueDate(self, customer):
        if self.calculateArrivalTime(customer) > customer.duedate:
            # print('Due Date')
            return False
        return True
    
    def canMakeBackToDepotFromCustomer(self, customer):
        if self.calculateArrivalTime(customer) + customer.servicetime + self.calculateArrivalTimeToDepot(customer) > self.max_time:
            # print('Service Time')
            return False
        return True

    def canFit(self, customer):
        return self.current_load + customer.demand <= self.capacity

    def waitForCustomer(self, customer):
        self.current_time = customer.readytime

    def canVisitAnyOf(self, customers):
        for customer in customers:
            if self.canVisit(customer):
                return True
        return False

    def visit(self, customer):
        self.current_load += customer.demand
        self.current_time = self.calculateArrivalTime(customer) + customer.servicetime
        #! MUST BE THE LAST LINE
        self.route.append(customer)
    
    def printRoute(self, idx=None):
        if idx:
            print(f'Route {idx}:', end=' ')
        else:
            print('Route:', end=' ')
        for customer in self.route:
            print(f'{customer.custno}, ', end=' ')
    
    def routeToString(self):
        route = ''
        for customer in self.route:
            route += f'{customer.custno}, '
        return route
    

# Vehicle class without speed attribute
class Vehicle2:
    def __init__(self, capacity, depot):
        self.capacity = capacity
        self.route: List[Customer] = []
        self.depot = depot
        self.max_time = self.depot.duedate
        self.current_load = 0
        self.current_time = 0
    
    def calculateRouteDistance(self):
        distance = 0
        for i in range(1, len(self.route)):
            distance += self.route[i-1].calculateDst(self.route[i])
        return distance

    def calculateDistance(self, next_customer):
        return self.route[-1].calculateDst(next_customer)
    
    # TODO Check if this is correct
    def canVisit(self, customer):
        if (self.current_load + customer.demand) > self.capacity:
            # print('Capacity')
            return False
        if self.current_time > customer.duedate:
            # print('Due Date')
            return False
        if self.current_time < customer.readytime:
            # print('Ready Time')
            return False
        if (self.current_time + customer.servicetime) > self.max_time:
            # print('Service Time')
            return False
        return True
    
    def canVisitInReadyTime(self, customer):
        if self.current_time < customer.readytime:
            # print('Ready Time')
            return False
        return True
    
    def canVisitBeforeDueDate(self, customer):
        if self.current_time > customer.duedate:
            # print('Due Date')
            return False
        return True
    
    def canMakeBackToDepotFromCustomer(self, customer):
        if (self.current_time + customer.servicetime) > self.max_time:
            # print('Service Time')
            return False
        return True

    def canFit(self, customer):
        return self.current_load + customer.demand <= self.capacity

    def waitForCustomer(self, customer):
        self.current_time = customer.readytime

    def canVisitAnyOf(self, customers):
        for customer in customers:
            if self.canVisit(customer):
                return True
        return False

    def visit(self, customer):
        self.current_load += customer.demand
        self.current_time += customer.servicetime
        #! MUST BE THE LAST LINE
        self.route.append(customer)
    
    def printRoute(self, idx=None):
        if idx:
            print(f'Route {idx}:', end=' ')
        else:
            print('Route:', end=' ')
        for customer in self.route:
            print(f'{customer.custno}, ', end=' ')
    
    def routeToString(self):
        route = ''
        for customer in self.route:
            route += f'{customer.custno}, '
        return route