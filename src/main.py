
# ------------------------------------------------------------------
#                           PRZEBIEG PROGRAMU
# ------------------------------------------------------------------

# wczytaj argumenty wejsciowe (liczbe populacji i iteracji, koszty)
# wczytaj polozenia punktow (miast i elektrowni)
# wygeneruj populacje poczatkowa
# przeprowadz kolejne iteracje algorytmu heurystycznego
# wygeneruj raport koncowy
#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from data_reader import DataReader
from heuristics import Heuristics

powers_coord = DataReader().read_locations("../res/powerstations-locations.txt")
cities_coord = DataReader().read_locations("../res/cities-locations.txt")
#args = dr.DataReader.read_arguments()
args = [20, 2, 20, 1.2, 0.7]
# args[0] - initial population size
# args[1] - selection size
# args[2] - number of iterations
# args[3] - cost_traction
# args[4] - cost_power_lines


heur_alg = Heuristics(cities_coord, powers_coord, args[0], args[1], args[2], args[3], args[4])
heur_alg.run_heuristics()

