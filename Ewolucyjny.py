import numpy as np
#import pandas as pd
import random as rd

#klasa rozwiazania
class Result:

    def __init__(self, x):
        self.parameters = x
        self.result = 0

class Evolution:

    def __init__(self, x_min, x_max, number_of_iteration =100,s =2 , n=20, size_of_elite=1,
                 offspring_population_size =20, p_mutation = 0.1, p_cross = 0.7):
        #value_function jest funkcja oceny rozwiazan
        #self.value_function = value_function
        #x_min i x_max sa wektorami
        self.parameter_min = x_min
        self.parameter_max = x_max
        #TO DO: n zalezne od ilosci parametrow
        #TO DO: ustawić ziarno generatoa
        self.number_of_iteration=number_of_iteration
        self.offspring =[]
        self.temporary_population=[]
        self.results = []
        self.size_of_elite=size_of_elite
        self.n = n
        self.s=s
        self.offspring_population_size = offspring_population_size
        self.p_mutation = p_mutation
        self.p_cross = p_cross

    def compute_population_size(self):
        return len(self.parameter_min)*10

    def init_population(self):
        for i in range(self.n):
            params = []
            for j in range(len(self.parameter_min)):
                params.append(rd.uniform(self.parameter_min[j], self.parameter_max[j]))
            self.results.append(Result(params))

    def execute(self):
        #TO DO:
        iteration_counter =0
        self.init_population()
        while iteration_counter < self.number_of_iteration:
            self.reproduction()
            self.perform_crossing_over()
            self.perform_mutation(self.offspring)
            #można rozważyć też mutacje populacji bazowej
            self.succession_with_substitution()
            iteration_counter+=1;

    def perform_crossing_over(self):
        while len(self.temporary_population)>0:
            first_parent = self.create_parent()
            second_parent = self.create_parent()
            random_number= rd.uniform(0,1)#usunąć magic number
            if random_number< self.p_cross:
                self.crossing_over(first_parent,second_parent)
            else:
                self.offspring.extend([first_parent,second_parent])


    def create_parent(self):
        parent_index = rd.randint(0, len(self.temporary_population)-1)
        parent = self.temporary_population[parent_index]
        self.temporary_population.pop(parent_index)
        return parent


    def crossing_over(self, parent1:Result , parent2: Result):
        cross_point = 1#rd.randint(0, len(parent1.parameters))
        #  to bym usunął skoro p-stwo krzyżowania jest ustalone to nie możemy tutaj losować punktu
        # z <0,2> bo wtedy to p-stwo będzie mniejsze dla 0,1 tak naprawdę tego krzyżowania nie będzie
        child1_parameters = parent1.parameters[:cross_point]
        child2_parameters = parent2.parameters[:cross_point]
        child1_parameters += parent2.parameters[cross_point:]
        child2_parameters += parent1.parameters[cross_point:]
        child1=Result(child1_parameters)
        child2=Result(child1_parameters)
        self.offspring.extend([child1,child2])

    def perform_mutation(self, population):
        for i in range(self.offspring_population_size):
            self.mutation_per_gene(population[i])

    def mutation(self, chromosome):
        mutate_point = rd.randint(0, len(chromosome))
        chromosome[mutate_point] = max(self.parameter_min[mutate_point],
            min(chromosome[mutate_point] + rd.normalvariate(0, 1), self.parameter_max[mutate_point]))
        # a czeu nie można odjąć ?
        # po jakimś czasie będą wszędzie 1
        # trzeba coś z tym rozkładem normalnym zrobić, częśto będzie dawał wartości ujemne - ja bym go przesunął w prawo


    def mutation_per_gene(self,chromosome :Result):
        for i in range(len(chromosome.parameters)):
            random_number = rd.uniform(0, 1)  # usunąć magic number
            if random_number<self.p_mutation:
                chromosome.parameters[i] = max(self.parameter_min[i],
                                               min(chromosome.parameters[i] + rd.normalvariate(0, 1),self.parameter_max[i]))

    def elite_succession(self):
        elite=[]
        new_parent_population =[]
      #  self.compute_fitnes_function()
        self.sort_populations()
        new_parent_population.extend(self.results[1:self.size_of_elite])
        new_parent_population.extend(self.offspring[1:(self.n-self.size_of_elite)])


    def sort_populations(self):
        self.results.sort(key=lambda result: result.result)
        self.offspring.sort(key=lambda result: result.result)

    def succession_with_substitution(self):
        self.compute_fitnes_function()
        self.results.extend(self.offspring)
        self.results.sort(key=lambda result: result.result) # sortuje malejąco
        self.results= self.results[1:self.n]

    def reproduction(self):
        probabilities = []
        tresholds=[]
        #sortowanie populacji bazowej
        self.offspring.clear()
        self.temporary_population.clear()
        for i in range(self.n):
            probabilities.append(self.compute_probability(self.n-i))
            tresholds.append(self.compute_treshold(probabilities))

        self.fill_temporary_population(tresholds)


    def fill_temporary_population(self, tresholds):
        while len(self.temporary_population) < self.offspring_population_size:
            random_number = rd.uniform(0, 1)
            for i in range(len(tresholds)):
                if random_number < tresholds[i]:
                    self.temporary_population.append(self.results[i])
                    break

    def compute_treshold(self, probabilities):
        treshold=0
        for i in range(len(probabilities)):
            treshold+=probabilities[i]
        return  treshold


    def compute_probability(self,rank):
       # return 2-self.s +2*(self.s-1)*((rank-1)/(self.n-1))
        return ((2-self.s)/self.n)+((2*(rank-1)*(self.s-1))/(self.n*(self.n-1)))

    def compute_fitnes_function(self):
        #ToDo: obliczanie wartości funkcji przystosowania
        for i in range(len(self.results)):
            self.results[i].result = self.results[i].parameters[0]

if __name__ == '__main__':
    algorithm= Evolution(x_min =[0, 0],x_max= [1, 1])
    algorithm.execute()
