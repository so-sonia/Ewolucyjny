import numpy as np
#import pandas as pd
import random as rd

#klasa rozwiazania
class Result:

    def __init__(self, x):
        self.parameters = x
        self.result = 0
    #TO DO: dodac operatory porownawcze, by umozliwic sortowanie


class Evolution:

    def __init__(self, value_function, x_min, x_max, n=20, p_mutation = 0.1, p_cross = 0.7):
        #value_function jest funkcja oceny rozwiazan
        self.value_function = value_function
        #x_min i x_max sa wektorami
        self.parameter_min = x_min
        self.parameter_max = x_max
        #TO DO: n zalezne od ilosci parametrow
        self.n = n
        self.p_mutation = p_mutation
        self.p_cross = p_cross

    def init_population(self):
        self.results = []

        for i in range(self.n):
            params = []
            for j in range(len(self.parameter_min)):
                params[j] = rd.random(self.parameter_min[j], self.parameter_max[j])
            self.results.add(Result(params))

    def execute(self):
        #TO DO:
        self.init_population()

    def crossing_over(self, parent1, parent2):
        cross_point = rd.randint(0, len(parent1))
        child1 = parent1[:cross_point]
        child2 = parent2[:cross_point]
        child1 += parent2[cross_point:]
        child2 += parent1[cross_point:]

    def mutation(self, chromosome):
        mutate_point = rd.randint(0, len(chromosome))
        #TO DO: losowana wartosc z rokladu normalnego
        chromosome[mutate_point] = max(self.parameter_min[mutate_point],
            min(chromosome[mutate_point] + rd.normalvariate(), self.parameter_max[mutate_point]))

    def reproduction(self):

    def succession(self):