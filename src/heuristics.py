from raport_generator import RaportGenerator
from structures import NetworkTree, LineSegment
from random import sample, random, shuffle, uniform
from numpy.random import choice
from bisect import bisect_left
from utils import two_pts_dist
import copy


class Heuristics:
    def __init__(self, cities_coords, powers_coords, pop_quantity, sel_size, members_to_discard, iter_quantity, mut_prob, cost_traction,
                 cost_power_lines):
        self.population = []
        self.is_population_sorted = False
        self.cities_coords = cities_coords
        self.powers_coords = powers_coords
        self.pop_quantity = pop_quantity
        self.sel_size = sel_size
        self.members_to_discard = members_to_discard
        self.mut_prob = mut_prob
        self.iter_quantity = iter_quantity
        self.cost_traction = cost_traction
        self.cost_power_lines = cost_power_lines
        self.generate_initial_population()
        self.raport_gen = RaportGenerator()

    def run_heuristics(self, raport_out_dir, filename):
        best_individuals = []

        for i in range(self.iter_quantity):
            output = self.do_heuristic_iteration()
            best_individuals.append(output[0])

            # tymczasowe info
            print str(i + 1) + "    |   " + "Best indiv: " + str(output[0]) + " |   " + "Avg cost: " + str(output[1])\
                  + " |   " + "Avg selected cost: " + str(output[2]) + " |   " + "Avg gen cost: " + str(output[3])

        # generate end raport
        print "\n++++++++++++++++++++++++++++++++++++++++++++++++\n"

        self.raport_gen.plot_iterations(self.iter_quantity,
                                        best_individuals,
                                        raport_out_dir,
                                        filename)

        self.raport_gen.print_best_individual(self.best_individual(),
                                              self.cities_coords,
                                              self.powers_coords,
                                              self.cost_traction,
                                              self.cost_power_lines,
                                              raport_out_dir,
                                              filename)


    def do_heuristic_iteration(self):
        best_cost = 0.0
        avg_cost = 0.0
        avg_selected_cost = 0.0
        avg_generated_cost = 0.0

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

        #generate iteration raport
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

    def crossover(self, individuals):
        iter = self.members_to_discard
        cross_list = []
        to_crossover = self.generate_pairs(individuals)

        for i in range(iter):
            indiv1 = to_crossover[2 * i]
            indiv2 = to_crossover[2 * i + 1]

            merged = self.get_adjusted_merged_network(indiv1, indiv2)

            powers_to_city_out = self.check_powers_to_city_conn(merged)
            merged = powers_to_city_out[0]
            powers_to_city = powers_to_city_out[1]

            connections = self.gen_conn_dict(merged)

            forest = self.gen_span_tree(connections)
            forest = self.add_rest_of_powers(forest, powers_to_city)
            forest = self.update_powers_link(forest)
            forest.count_goal_func(self.cost_traction, self.cost_power_lines)

            cross_list.append(forest)

        return cross_list

    def mutation(self, individuals):
        for indiv in individuals:
            if uniform(0.0, 1.0) < self.mut_prob:
                indiv.mutate()

        return individuals

    def succession(self, mutated):
        self.population.sort(key=lambda x: x.goal_func, reverse=True)
        for i in range(self.members_to_discard):
            self.population.pop()

        mutated.sort(key=lambda x: x.goal_func, reverse=True)
        for i in range(self.members_to_discard):
            self.population.append(mutated[i])

    def best_individual(self, rank=0):
        if rank >= len(self.population):
            rank = len(self.population) - 1
        if self.is_population_sorted is False:
            self.population.sort(key=lambda individual: individual.goal_func,
                                 reverse=True)
            self.is_population_sorted = True
        return self.population[rank]

    def generate_pairs(self, individuals):
        pair_list = []
        num = 2 * self.members_to_discard
        to_add = len(individuals)

        while(num > 0):
            num -= to_add
            if num < 0:
                to_add += num
            shuffle(individuals)
            pair_list += individuals[0:to_add]

        return pair_list


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
            probability = 0
            pow_bonus = 0

            seg_prob = 1 / (two_pts_dist(point1 + (0,), point2 + (0,)) * self.cost_traction)

            for pow_len in seg.powers_line_segment_len:
                if pow_len >= 1:
                    pow_bonus += (1 / pow_len)
                else:
                    pow_bonus += 1

            probability = seg_prob + seg_prob * pow_bonus * (self.cost_traction / self.cost_power_lines)

            connections.get(point1).append([seg, probability])
            connections.get(point2).append([seg, probability])

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
            pick = None
            probabilities = []
            to_pick_from = []
            sum_of_unpicked = 0

            for point in usedSet:
                shuffle(connections.get(point))

                for el in connections.get(point):
                    points = el[0].points.copy()
                    points.remove(point)
                    end_point = points.pop()

                    # if end_point in unusedSet and el[1] < min_val:
                    #     min_val = el[1]
                    #     pick = el[0]

                    if end_point in unusedSet:
                        to_pick_from.append(el[0])
                        probabilities.append(el[1])
                        sum_of_unpicked += el[1]

            for i in range(len(probabilities)):
                probabilities[i] /= sum_of_unpicked

            pick = choice(to_pick_from,1,probabilities)[0]
            forest.add_new_segment(pick)

            points = pick.points.copy()
            point1 = points.pop()
            point2 = points.pop()
            if point1 in unusedSet:
                unusedSet.remove(point1)
                usedSet.add(point1)
            else:
                unusedSet.remove(point2)
                usedSet.add(point2)

        return forest

    def check_pop_con(self, population):
        error_idx = []
        i = 0
        for ind in population:
            res = self.check_conn(ind)
            if(res == False):
                error_idx.append(i)
            i+=1

        return len(error_idx) == 0

    def check_conn(self, network):
        powers = set()
        for seg in network.segments:
            if seg.conn_to_powerstation == True:
                for coord in seg.powers_coord:
                    powers.add(coord)

        return len(powers) == len(self.powers_coords)

    def check_powers_missing(self, network):
        powers = set()
        for seg in network.segments:
            if seg.conn_to_powerstation == True:
                for coord in seg.powers_coord:
                    powers.add(coord)

        ret_set = copy.deepcopy(self.powers_coords)
        ret_set = ret_set.difference(powers)

        return ret_set

    def count_avg_cost(self, population):
        cost = 0.0
        for individual in population:
            cost += individual.goal_func

        return cost / len(population)

    def check_powers_to_city_conn(self, merged):
        powers_to_city = {}

        for seg in merged.segments:
            points = seg.points.copy()
            point1 = points.pop()
            point2 = points.pop()

            if seg.conn_to_powerstation == True:
                # sprawdz polaczenia do miast
                last_index = len(seg.powers_line_segment) - 1
                for i in range(last_index + 1):
                    power_points = seg.powers_line_segment[last_index - i].points.copy()
                    city_point = None
                    if point1 in power_points:
                        city_point = point1
                    if point2 in power_points:
                        city_point = point2
                    # jezeli elektrownia polaczona z miastem
                    if city_point != None:
                        power_point = seg.powers_coord[last_index - i]
                        powers_to_city[power_point] = []
                        powers_to_city[power_point].append(copy.deepcopy(seg.powers_line_segment[last_index - i]))
                        powers_to_city[power_point].append(seg.powers_line_segment_len[last_index - i])
                        del seg.powers_coord[last_index - i]
                        del seg.powers_line_segment[last_index - i]
                        del seg.powers_line_segment_len[last_index - i]

                if len(seg.powers_line_segment) == 0:
                    seg.conn_to_powerstation = False

        return [merged, powers_to_city]

    def add_rest_of_powers(self,forest, powers_to_city):
        # dodaj polaczenia elektrowni do miast
        for key in powers_to_city:
            val = powers_to_city.get(key)
            idx = 0
            max = -1
            for i in range(len(forest.segments)):
                points = forest.segments[i].points.copy()
                point1 = points.pop()
                point2 = points.pop()

                if point1 in val[0].points or point2 in val[0].points:
                    if len(forest.segments[i].powers_line_segment) > max:
                        max = len(forest.segments[i].powers_line_segment)
                        idx = i

            if len(forest.segments[idx].powers_line_segment) == 0:
                forest.segments[idx].conn_to_powerstation = True

            forest.segments[idx].powers_coord.append(key)
            forest.segments[idx].powers_line_segment.append(val[0])
            forest.segments[idx].powers_line_segment_len.append(val[1])

        powers_missing = self.check_powers_missing(forest)

        for pow in powers_missing:
            forest.connect_power_plant(pow)

        return forest


    def update_powers_link(self, forest):
        for seg in forest.segments:
            if seg.conn_to_powerstation == True:
                for coord in seg.powers_coord:
                    forest.plant_to_seg[coord] = seg

        return forest

