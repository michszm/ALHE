from raport_generator import RaportGenerator
from structures import NetworkTree, LineSegment
from random import sample
from random import random, shuffle
from bisect import bisect_left
import sys
import copy


<<<<<<< HEAD
class Heuristics:
    def __init__(self, cities_coords, powers_coords, pop_quantity, sel_size, iter_quantity, cost_traction,
                 cost_power_lines):
        self.population = []
        self.is_population_sorted = False
=======
    def __init__(self, cities_coords, powers_coords, pop_quantity, sel_size, elitism, mut_prob, iter_quantity, cost_traction, cost_power_lines):
>>>>>>> 1a1a2c763efd798dbe39a059119dfb71bd9a77a4
        self.cities_coords = cities_coords
        self.powers_coords = powers_coords
        self.pop_quantity = pop_quantity
        self.sel_size = sel_size
        self.elitism = elitism
        self.mut_prob = mut_prob
        self.iter_quantity = iter_quantity
        self.cost_traction = cost_traction
        self.cost_power_lines = cost_power_lines
        self.generate_initial_population()
        self.raport_generator = RaportGenerator()

    def run_heuristics(self):
        for i in range(self.iter_quantity):
            output = self.do_heuristic_iteration()

            # tymczasowe info
            print str(i + 1) + "    |   " + "Best indiv: " + str(output[0]) + " |   " + "Avg cost: " + str(output[1])\
                  + " |   " + "Avg selected cost: " + str(output[2]) + " |   " + "Avg gen cost: " + str(output[3])

        # generate end raport
        print "\n++++++++++++++++++++++++++++++++++++++++++++++++\n"

    def do_heuristic_iteration(self):
<<<<<<< HEAD
        best_cost = 0.0
        avg_cost = 0.0
        avg_selected_cost = 0.0
        avg_generated_cost = 0.0
=======
        selected_individuals = self.selection(self.sel_size)
        post_crossover_population = self.crossover()
        post_mutation_population = self.mutation(post_crossover_population, self.mut_prob)
        self.population = self.succession(self.elitism, post_mutation_population)
        print "Iteration"
        #generate iteration raport
>>>>>>> 1a1a2c763efd798dbe39a059119dfb71bd9a77a4

        sel_individuals = self.selection(self.sel_size)
        avg_selected_cost = self.count_avg_cost(sel_individuals)

        crossovered = self.crossover(sel_individuals)

        mutated = self.mutation(crossovered)
        avg_generated_cost = self.count_avg_cost(mutated)

        self.succession(mutated)
        avg_cost = self.count_avg_cost(self.population)

        # podczas selekcji zbior jest sortowany, wybierz pierwszego
        # (najlepszego) osobnika
        best_cost = self.population[0].goal_func

        # generate iteration raport
        return [best_cost, avg_cost, avg_selected_cost, avg_generated_cost]


    def generate_initial_population(self):
        # generuj populacje poczatkowa
        for i in range(self.pop_quantity):

            individual = NetworkTree()

            usedSet = set()
            unusedSet = set()
            for point in self.cities_coords:
                unusedSet.add(point)

            while len(unusedSet) != 0:

                point = sample(unusedSet, 1)
                point = point.pop(0)
                unusedSet.remove(point)

                if len(usedSet) == 0:
                    usedSet.add(point)

                else:
                    usedPoint = sample(usedSet, 1)
                    usedPoint = usedPoint.pop(0)
                    individual.add_new_segment(LineSegment(point, usedPoint))
                    usedSet.add(point)

            for coord in self.powers_coords:
                individual.connect_power_plant(coord)

            individual.count_goal_func(self.cost_traction,
                                       self.cost_power_lines)

            self.population.append(individual)

    def selection(self, size):
        acc_goal_funcs = list()
        last_goal_func = 0
        for individual in self.population:
            last_goal_func = individual.goal_func + last_goal_func
            acc_goal_funcs.append(last_goal_func)
        sel_individuals = list()
        sel_pos = None
        for i in range(size):
            rand_goal_func = random() * acc_goal_funcs[-1]
            if rand_goal_func in acc_goal_funcs:
                sel_pos = acc_goal_funcs.index(rand_goal_func)
            else:
                sel_pos = bisect_left(acc_goal_funcs, rand_goal_func)
            sel_individuals.append(self.population[sel_pos])

        return sel_individuals

<<<<<<< HEAD
    def crossover(self, individuals):
        iter = len(individuals) / 2
        cross_list = []
        shuffle(individuals)

        for i in range(iter):
            indiv1 = individuals[2 * i]
            indiv2 = individuals[2 * i + 1]

            merged = self.get_adjusted_merged_network(indiv1, indiv2)
            connections = self.gen_conn_dict(merged)
            forest = self.gen_span_tree(connections)
            cross_list.append(forest)

        return cross_list

    def mutation(self, individuals):
        for indiv in individuals:
            indiv.mutate()

        return individuals

    def succession(self, mutated):
        for indiv in mutated:
            self.population.append(indiv)

        self.population.sort(key=lambda x: x.goal_func, reverse=True)
        to_delete = len(self.population) - self.pop_quantity

        for i in range(to_delete):
            self.population.pop()
=======
    def crossover(self):
        print "Crossover"
        # quick fix
        return []

    def mutation(self, individuals, probability):
        out_individuals = list()
        for individual in individuals:
            if random() < float(probability):
                out_individuals.append(individual.mutate())
            else:
                out_individuals.append(individual)
        return out_individuals

    def succession(self, kept_curr_best, crossover_pop):
        next_population = []
        for i in range(kept_curr_best):
            if i < len(self.population):
                next_population.append(self.best_individual(kept_curr_best))
        next_population += crossover_pop
        return next_population
>>>>>>> 1a1a2c763efd798dbe39a059119dfb71bd9a77a4

    def best_individual(self, rank=0):
        if rank >= len(self.population):
            rank = len(self.population) - 1
        if self.is_population_sorted is False:
            self.population.sort(key=lambda individual: individual.goal_func,
                                 reverse=True)
            self.is_population_sorted = True
        return self.population[rank]

    def merge_parents(self, indiv1, indiv2):
        seg_len = len(indiv1.segments)
        merged = NetworkTree()

        for seg_num in range(seg_len):
            merged.add_new_segment(copy.deepcopy(indiv1.segments[seg_num]))
            merged.add_new_segment(copy.deepcopy(indiv2.segments[seg_num]))

        return merged

    def init_minimal_cost_dict(self):
        powers_min = {}

        # przygotuj zmienne do minimalnych kosztow polaczen dla kazdej elektrowni
        for coord in self.powers_coords:
            ls = LineSegment((0, 0), (0, 0))
            ls.conn_to_powerstation = True
            ls.powers_line_segment.append(None)
            ls.powers_line_segment_len.append(float("inf"))
            ls.powers_coord.append(coord)
            powers_min[coord] = ls

        return powers_min

    def pick_best_power_conn(self, merged, powers_min):
        powerstations = NetworkTree()
        # wybierz najlepsze krawedzie dla elektrowni
        for seg in merged.segments:
            if seg.conn_to_powerstation == True:
                for i in range(len(seg.powers_line_segment)):
                    # jezeli dla minmum od punktu elektrowni
                    point = seg.powers_coord[i]
                    if seg.powers_line_segment_len[i] < powers_min.get(point).powers_line_segment_len[0]:
                        powers_min.get(point).points = seg.points.copy()
                        powers_min.get(point).powers_line_segment[0] = seg.powers_line_segment[i]
                        powers_min.get(point).powers_line_segment_len[0] = seg.powers_line_segment_len[i]

        # polacz najlepsze krawedzie (merge)
        for key1, val1 in powers_min.items():
            powers_min.pop(key1)
            # sprawdz czy jakies z pozostalych polaczen
            for key2, val2 in powers_min.items():
                if val1.conn_to_powerstation == True and val2.conn_to_powerstation == True:
                    if val1 == val2:
                        val1.powers_line_segment.append(val2.powers_line_segment[0])
                        val1.powers_line_segment_len.append(val2.powers_line_segment_len[0])
                        val1.powers_coord.append(val2.powers_coord[0])
                        powers_min.get(key2).conn_to_powerstation = False

            if val1.conn_to_powerstation == True:
                powerstations.add_new_segment(val1)

        for seg in powerstations.segments:
            merged.segments.remove(seg)

        return [powerstations, merged]

    def clean_powerstations(self, merged):

        # wyczysc stare polaczenia z elektrowniami
        for i in range(len(merged.segments)):
            if merged.segments[i].conn_to_powerstation == True:
                merged.segments[i].conn_to_powerstation = False
                merged.segments[i].powers_line_segment = []
                merged.segments[i].powers_line_segment_len = []
                merged.segments[i].powers_coord = []

        return merged

    def get_adjusted_merged_network(self, indiv1, indiv2):

        temp = set()

        merged = self.merge_parents(indiv1, indiv2)
        powers_min = self.init_minimal_cost_dict()
        pick_powers = self.pick_best_power_conn(merged, powers_min)

        powers = pick_powers[0]
        merged = pick_powers[1]

        # usun z merged stare elektrownie oraz duplikaty krawedzi o tych samych wspolrzednych
        merged = self.clean_powerstations(merged)

        for pow in powers.segments:
            temp.add(pow)

        for seg in merged.segments:
            temp.add(seg)

        merged = NetworkTree()

        for val in temp:
            merged.add_new_segment(val)

        return merged

    def gen_conn_dict(self, merged):
        connections = {}
        for city in self.cities_coords:
            connections[city] = []

        for seg in merged.segments:
            points = seg.points.copy()
            point1 = points.pop()
            point2 = points.pop()

            if seg.conn_to_powerstation == True:
                cost = 0
            else:
                cost = sys.float_info.max - 1

            connections.get(point1).append([seg, cost])
            connections.get(point2).append([seg, cost])

        return connections

    def gen_span_tree(self, connections):
        usedSet = set()
        unusedSet = set()
        unusedSet = self.cities_coords.copy()

        forest = NetworkTree()
        start_point = sample(unusedSet, 1).pop()

        usedSet.add(start_point)
        unusedSet.remove(start_point)

        # algorytm Prima do generowania drzewa rozpinajacego
        while (len(unusedSet) != 0):

            picked_seg = None
            picked_end_point = None
            min_val = float("inf")

            for point in usedSet:
                shuffle(connections.get(point))

                for el in connections.get(point):
                    points = el[0].points.copy()
                    points.remove(point)
                    end_point = points.pop()

                    if el[1] < min_val and end_point in unusedSet:
                        min_val = el[1]
                        picked_seg = el[0]
                        picked_end_point = end_point

            forest.add_new_segment(picked_seg)
            unusedSet.remove(picked_end_point)
            usedSet.add(picked_end_point)

        forest.count_goal_func(self.cost_traction, self.cost_power_lines)

        return forest

    def check_conn(self, network):
        powers = set()
        for seg in network.segments:
            if seg.conn_to_powerstation == True:
                for coord in seg.powers_coord:
                    powers.add(coord)

        return len(powers) == len(self.powers_coords)

    def count_avg_cost(self, population):
        cost = 0.0
        for individual in population:
            cost += individual.goal_func

        return cost / len(population)