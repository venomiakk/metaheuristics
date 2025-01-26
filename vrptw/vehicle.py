from typing import List
from customer import Customer

class Vehicle:
    def __init__(self, capacity, depot, speed=50):
        self.capacity = capacity
        self.route: List[Customer] = []
        self.speed = speed / 10 #! need to experiment with this
        self.depot = depot
        self.max_time = self.depot.duedate
        self.current_load = 0
        self.current_time = 0

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