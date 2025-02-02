from typing import List
from customer import Customer


class Vehicle:
    def __init__(self, capacity, depot):
        self.capacity = capacity
        self.route: List[Customer] = []
        self.depot = depot
        self.max_time = self.depot.duedate
        self.current_load = 0
        self.current_time = 0
        self.fitness = float('inf')

    def visit(self, customer):
        self.current_load += customer.demand
        self.current_time += customer.servicetime
        #! MUST BE THE LAST LINE
        self.route.append(customer)

    def getTimeViolations(self):
        time_violations = 0
        for i in range(1, len(self.route) - 1):
            if (self.route[i].servicetime + self.route[i].readytime) > self.route[i+1].duedate:
                time_violations += 1
        return time_violations
    
    def getCapacityViolation(self):
        route_load = 0
        for i in range(1, len(self.route) - 1):
            route_load += self.route[i].demand
        
        return max(0, route_load - self.capacity)

    def isRouteCorrect(self):
        if self.route[0] != self.depot or self.route[-1] != self.depot:
            return False
        route_load = 0
        for i in range(1, len(self.route) - 1):
            route_load += self.route[i].demand
            if route_load > self.capacity:
                return False
            if (self.route[i].servicetime + self.route[i].readytime) > self.route[i+1].duedate:
                return False
        return True

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