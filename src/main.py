# ------------------------------------------------------------------
#
# ------------------------------------------------------------------

from data_reader import DataReader
from heuristics import Heuristics
import datetime
import os

config_file_path = "../res/config/"
tests_file_path = "../res/tests/"
raport_figures_file_path = "../res/raport_figures/"

format = "%Y_%m_%d_%H_%M_%S"
date_of_test = datetime.datetime.today().strftime(format)
raport_out_dir = raport_figures_file_path + "raport_" + date_of_test
config_file_name = "tests_config.txt"

test_files = DataReader().read_config(config_file_path + config_file_name)
os.mkdir(raport_out_dir)

print "Start test"
print "Begin test time: "  + date_of_test

for test in test_files:
    cities_coord = DataReader().read_locations(tests_file_path + test[0])
    powers_coord = DataReader().read_locations(tests_file_path + test[1])
    args = DataReader().read_arguments(tests_file_path + test[2])

    for arg in args:
        print "Start test case: " + test[2][:6]
        print "Run test with arguments: " + str(arg[0]) + ", " + str(arg[0] - arg[1]) + ", " \
              + str(arg[2]) + ", " + str(arg[3]) + ", " + str(arg[4]) + ", " + str(arg[5]) + "\n"

        heur_alg = Heuristics(cities_coord, powers_coord, arg[0], arg[0], arg[0] - arg[1], arg[2], arg[3], arg[4], arg[5])
        heur_alg.run_heuristics(raport_out_dir, test[2][:6])