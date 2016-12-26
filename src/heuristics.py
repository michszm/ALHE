from raport_generator import RaportGenerator
from structures import NetworkTree, LineSegment
import random

class Heuristics:

    population = []

    def __init__(self, cities_coord, powers_coord, pop_quantity, iter_quantity, cost_traction, cost_power_lines):
        self.cities_coord = cities_coord
        self.powers_coord = powers_coord
        self.pop_quantity = pop_quantity
        self.iter_quantity = iter_quantity
        self.cost_traction = cost_traction
        self.cost_power_lines = cost_power_lines
        self.generate_initial_population()
        self.raport_generator = RaportGenerator()


    def run_heuristics(self):
        for i in range(self.iter_quantity):
            print i
            self.do_heuristic_iteration()
            print "Main loop"
            #generate end raport

    def do_heuristic_iteration(self):
        self.selection()
        self.crossover()
        self.mutation()
        self.succession()
        print "Iteration"
        #generate iteration raport

    def generate_initial_population(self):

        # generuj populacje poczatkowa
        for i in range(self.pop_quantity):

            individual = NetworkTree()

            usedSet = set()
            unusedSet = set()
            for point in self.cities_coord:
                unusedSet.add(point)

            while len(unusedSet) != 0:

                point = random.sample(unusedSet, 1)
                point = point.pop(0)
                unusedSet.remove(point)

                if len(usedSet) == 0:
                    usedSet.add(point)

                else:
                    usedPoint = random.sample(usedSet,1)
                    usedPoint = usedPoint.pop(0)
                    individual.addNewSegment(LineSegment(point, usedPoint))
                    usedSet.add(point)

            self.population.append(individual)


    def selection(self):
        print "Selection"

    def crossover(self):
        print "Crossover"

    def mutation(self):
        print "Mutation"

    def succession(self):
        print "Succession"
