from raport_generator import RaportGenerator
from structures import NetworkTree, LineSegment
from utils import nrst_pt_on_seg
import random

class Heuristics:

    population = []
    is_population_sorted = False

    def __init__(self, cities_coords, powers_coords, pop_quantity, iter_quantity, cost_traction, cost_power_lines):
        self.cities_coords = cities_coords
        self.powers_coords = powers_coords
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
            for point in self.cities_coords:
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
                    individual.add_new_segment(LineSegment(point, usedPoint))
                    usedSet.add(point)

            for coord in self.powers_coords:
                min_dist = float("inf")
                min_dist_point = None
                for seg in individual.segments:
                    if seg.conn_to_powerstation is False:
                        pt, dist = nrst_pt_on_seg(coord + (0,),
                                                  seg.point1 + (0,),
                                                  seg.point2 + (0,))
                        if dist < min_dist:
                            min_dist = dist
                            min_dist_point = (pt[0], pt[1])
                if min_dist_point is not None:
                    powers_seg = LineSegment(min_dist_point, coord)
                    powers_seg.conn_to_powerstation = True
                    powers_seg.powers_line_segment_len = min_dist
                    powers_seg.powers_coord = coord
                    individual.add_new_segment(powers_seg)

            individual.count_goal_func(self.cost_traction,
                                       self.cost_power_lines)

            self.population.append(individual)


    def selection(self):
        print "Selection"

    def crossover(self):
        print "Crossover"

    def mutation(self):
        print "Mutation"

    def succession(self):
        print "Succession"

    def best_individual(self, rank=0):
        if rank >= len(self.population):
            rank = len(self.population) - 1
        if self.is_population_sorted is False:
            self.population.sort(key=lambda individual: individual.goal_func,
                                 reverse=True)
            self.is_population_sorted = True
        return self.population[rank]
