class DataReader:

    def read_config(self, file_name):
        file = open(file_name, "r")
        test_files = []

        for line in file:
            row = ("".join(line.split())).split(";")
            if row[0][0] != "#":
                test_files.append((row[0],row[1],row[2]))

        file.close()
        return test_files

    def read_locations(self, file_name):
        file = open(file_name, "r")
        coord = set()

        for line in file:
            row = line.split()
            coord.add((float(row[0]), float(row[1])))

        file.close()
        return coord

    def read_arguments(self, file_name):
        file = open(file_name, "r")
        args = []

        for line in file:
            row = ("".join(line.split())).split(",")
            args.append((int(row[0]), int(row[1]), int(row[2]), float(row[3]), float(row[4]), float(row[5]), int(row[6])))

        file.close()
        return args