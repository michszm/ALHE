
# ------------------------------------------------------------------
#
# ------------------------------------------------------------------

from data_reader import DataReader
from heuristics import Heuristics

config_file_path = "../res/config/"
tests_file_path = "../res/tests/"
raport_figures_file_path = "../res/raport_figures/"

config_file_name = "tests_config.txt"

test_files = DataReader().read_config(config_file_path + config_file_name)

for test in test_files:
    cities_coord = DataReader().read_locations(tests_file_path + test[0])
    powers_coord = DataReader().read_locations(tests_file_path + test[1])
    args = DataReader().read_arguments(tests_file_path + test[2])

    for arg in args:
        heur_alg = Heuristics(cities_coord, powers_coord, arg[0], arg[0], arg[0] - arg[1], arg[2], arg[3], arg[4], arg[5])
        heur_alg.run_heuristics(raport_figures_file_path + test[0][:6])

