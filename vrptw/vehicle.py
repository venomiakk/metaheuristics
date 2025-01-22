from typing import List
from customer import Customer

class Vehicle:
    def __init__(self, capacity, speed=50):
        self.capacity = capacity
        self.route: List[Customer] = []
        self.speed = speed
        self.current_load = 0
        self.current_time = 0

    def calculateArrivalTime(self, customer):
        dst = self.route[-1].calculateDst(customer)
        return (dst / self.speed) + self.current_time

    def calculateTimeToNextCustomer(self, customer):
        dst = self.route[-1].calculateDst(customer)
        return dst / self.speed