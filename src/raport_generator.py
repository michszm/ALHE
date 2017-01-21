from matplotlib import pyplot
import networkx as nx
import datetime

class RaportGenerator:

    def __init__(self):
        self.format = "%Y_%m_%d_%H_%M_%S_%f"

    def generate_report(self):
        print "Report"

    def plot_iterations(self, size, data, raport_out_dir, filename, params):
        figure, axes = pyplot.subplots()

        x = range(1, size + 1)
        y = data
        pyplot.xlabel('Numer iteracji (i)')
        pyplot.ylabel('Funkcja celu (O)')
        pyplot.title('Przebieg dzialania algorytmu')
        pyplot.plot(x, y, color='black', label='O(i)')

        x = range(0)
        y = range(0)
        pyplot.plot(x, y, color='white', label='P: ' + str(params[0])
                                                + '\nE: ' + str(params[1])
                                                + '\nI: ' + str(params[2])
                                                + '\nM: ' + str(params[3]))

        handles, labels = axes.get_legend_handles_labels()
        legend = axes.legend(handles, labels, loc='upper center', ncol=2, bbox_to_anchor=(0.5, -0.1))
        legend.get_frame().set_alpha(0.5)
        file_out = filename + '_' + datetime.datetime.today().strftime(self.format) + '_iterations.png'
        print "Generate iterations raport: \t\t" + file_out
        pyplot.savefig(raport_out_dir + "/" + file_out,
                       bbox_extra_artists=(legend,), bbox_inches='tight')
        pyplot.close(figure)

    def print_best_individual(self, individual, cities, powers,cost_traction, cost_power_lines, raport_out_dir, filename, params):
        figure, axes = pyplot.subplots()
        g = nx.Graph()

        traction_len, powers_len = individual.traction_powers_lengths()

        cityNodes = {i: i for i in cities}
        nx.draw_networkx_nodes(g, cityNodes, cityNodes.keys(), node_color='red', node_size=75, label='Miasto' + '\n'
                                                                                                     + 'DT: ' + str(format(traction_len, '.5f')) + '\n'
                                                                                                     + 'KT: ' + str(cost_traction) + '\n',
                                                                                                     ax=axes)
        powerNodes = {i: i for i in powers}
        nx.draw_networkx_nodes(g, powerNodes, powerNodes.keys(), node_color='yellow', node_size=25, label='Elektrownia' + '\n'
                                                                                                          + 'DE: ' + str(format(powers_len, '.5f')) + '\n'
                                                                                                          + 'KE: ' + str(cost_power_lines) + '\n',
                                                                                                          ax=axes)
        nullNodes = {(0, 0): (0, 0)}
        nx.draw_networkx_nodes(g, nullNodes, nullNodes.keys(), node_color='white', node_size=0, label='FC: ' + str(individual.goal_func)
                                                                                                             + '\nP: ' + str(params[0])
                                                                                                             + '\nE: ' + str(params[1])
                                                                                                             + '\nI: ' + str(params[2])
                                                                                                             + '\nM: ' + str(params[3]),
                                                                                                             ax=axes)

        for seg in individual.segments:
            if seg.conn_to_powerstation is True:
                for power_seg in seg.powers_line_segment:
                    points_set = power_seg.points.copy()
                    if len(points_set) == 2:
                        point1 = points_set.pop()
                        if not cityNodes.has_key(point1) and not powerNodes.has_key(point1):
                            pos = {point1: point1}
                            nx.draw_networkx_nodes(g, pos, pos.keys(), node_color='green', node_size=10, ax=axes)
                        point2 = points_set.pop()
                        if not cityNodes.has_key(point2) and not powerNodes.has_key(point2):
                            pos = {point2: point2}
                            nx.draw_networkx_nodes(g, pos, pos.keys(), node_color='green', node_size=10, ax=axes)
                        pos = {point1: point1, point2: point2}
                        nx.draw_networkx_edges(g, pos, [(point1, point2)], edge_color='green', ax=axes)
            points_set = seg.points.copy()
            point1 = points_set.pop()
            point2 = points_set.pop()
            pos = {point1: point1, point2: point2}
            nx.draw_networkx_edges(g, pos, [(point1, point2)], edge_color='black', ax=axes)

        pyplot.gca().set_aspect('equal', adjustable='box')
        pyplot.xlabel('x')
        pyplot.ylabel('y')
        pyplot.title('Najlepszy osobnik')
        handles, labels = axes.get_legend_handles_labels()
        legend = axes.legend(handles, labels, loc='upper center', ncol=3, bbox_to_anchor=(0.5, -0.1))
        legend.get_frame().set_alpha(0.5)
        file_out = filename + '_' + datetime.datetime.today().strftime(self.format) + '_best.png'
        print "Generate best individual raport: \t" + file_out
        pyplot.savefig(raport_out_dir + "/" + file_out,
                       bbox_extra_artists=(legend,), bbox_inches='tight')
        pyplot.close(figure)