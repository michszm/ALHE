
# ------------------------------------------------------------------
#
# ------------------------------------------------------------------

from data_reader import DataReader
from heuristics import Heuristics

<<<<<<< HEAD
config_file_path = "../res/config/"
tests_file_path = "../res/tests/"

config_file_name = "tests_config.txt"

test_files = DataReader().read_config(config_file_path + config_file_name)
=======
powers_coord = DataReader().read_locations("../res/powerstations-locations.txt")
cities_coord = DataReader().read_locations("../res/cities-locations.txt")
#args = dr.DataReader.read_arguments()
args = [20, 2, 1, 0.2, 20, 1.2, 0.7]
# args[0] - initial population size
# args[1] - selection size
# args[2] - elitism
# args[3] - mutation probability
# args[4] - number of iterations
# args[5] - cost_traction
# args[6] - cost_power_lines
>>>>>>> 1a1a2c763efd798dbe39a059119dfb71bd9a77a4

for test in test_files:
    cities_coord = DataReader().read_locations(tests_file_path + test[0])
    powers_coord = DataReader().read_locations(tests_file_path + test[1])
    args = DataReader().read_arguments(tests_file_path + test[2])

<<<<<<< HEAD
    for arg in args:
        heur_alg = Heuristics(cities_coord, powers_coord, arg[0], arg[1], arg[2], arg[3], arg[4])
        heur_alg.run_heuristics()
=======
heur_alg = Heuristics(cities_coord, powers_coord, args[0], args[1], args[2], args[3], args[4], args[5], args[6])
heur_alg.run_heuristics()
>>>>>>> 1a1a2c763efd798dbe39a059119dfb71bd9a77a4

