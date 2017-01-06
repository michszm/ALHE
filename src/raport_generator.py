from matplotlib import pyplot
import networkx as nx


class RaportGenerator:

    def __init__(self):
        print "Init report"

    def generate_report(self):
        print "Report"

    def plot_iterations(self, size, data):
        x = range(1, size + 1)
        y = data

        pyplot.xlabel('Numer iteracji (i)')
        pyplot.ylabel('Funkcja celu (O)')
        pyplot.title('Przebieg dzialania algorytmu')
        pyplot.plot(x, y, color='black', label='O(i)')
        pyplot.legend()
        pyplot.show()

    def print_best_individual(self, individual, cities, powers):
        g = nx.Graph()

        cityNodes = {i: i for i in cities}
        nx.draw_networkx_nodes(g, cityNodes, cityNodes.keys(), node_color='red', node_size=750, label='Miasto')

        powerNodes = {i: i for i in powers}
        nx.draw_networkx_nodes(g, powerNodes, powerNodes.keys(), node_color='yellow', node_size=250, label='Elektrownia')

        for seg in individual.segments:
            if seg.conn_to_powerstation is True:
                for power_seg in seg.powers_line_segment:
                    points_set = power_seg.points.copy()
                    if len(points_set) == 2:
                        point1 = points_set.pop()
                        if not cityNodes.has_key(point1) and not powerNodes.has_key(point1):
                            pos = {point1: point1}
                            nx.draw_networkx_nodes(g, pos, pos.keys(), node_color='green', node_size=50)
                        point2 = points_set.pop()
                        if not cityNodes.has_key(point2) and not powerNodes.has_key(point2):
                            pos = {point2: point2}
                            nx.draw_networkx_nodes(g, pos, pos.keys(), node_color='green', node_size=50)
                        pos = {point1: point1, point2: point2}
                        nx.draw_networkx_edges(g, pos, [(point1, point2)], edge_color='green')
            points_set = seg.points.copy()
            point1 = points_set.pop()
            point2 = points_set.pop()
            pos = {point1: point1, point2: point2}
            nx.draw_networkx_edges(g, pos, [(point1, point2)], edge_color='black')

        pyplot.xlabel('x')
        pyplot.ylabel('y')
        pyplot.title('Najlepszy osobnik')
        pyplot.legend()
        pyplot.show()
