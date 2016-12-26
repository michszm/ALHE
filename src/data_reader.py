class DataReader:

    def read_locations(self, file_name):
        file = open(file_name, "r")

        coord = []

        for line in file:
            row = line.split()
            coord.append((row[0], row[1]))

        file.close()
        return coord

    def read_arguments(self):
        pop_quantity = raw_input()
        iter_quantity = raw_input()
        cost_traction = raw_input()
        cost_power_lines =  raw_input()

        return [pop_quantity, iter_quantity, cost_traction, cost_power_lines]