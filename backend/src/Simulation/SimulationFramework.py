import sys
sys.path.append('.')
from Data.DataRetriever import DataRetriever
import random

class SimulationFramework:

    __current_day = 0
    __dataRetriever = None

    def __is_infected(self, node):
        return self.__current_day - self.__dataRetriever.G.nodes[node]["last_infection_time"] < 10

    def __probability_of_infection(self, node):
        my_sum = 0

        for neighbor in self.__dataRetriever.G.neighbors(node):
            is_already_infected = self.__is_infected(neighbor)
            my_sum += is_already_infected

        return my_sum / (len(list(self.__dataRetriever.G.neighbors(node))) * 5)

    def update_new_covid_cases(self):

        for node in self.__dataRetriever.G.nodes:

            if self.__current_day == 0:
                node_gets_infected = random.random() < 0.001
            else:
                is_already_infected = self.__is_infected(node)

                if not is_already_infected:
                    node_gets_infected = random.random() < self.__probability_of_infection(node)
                else:
                    continue

            if node_gets_infected == True:
                self.__dataRetriever.G.nodes[node]["last_infection_time"] = self.__current_day

    def run_rimulation(self):

        self.update_new_covid_cases()

        while True:
            
            # self.force_field(self.__dataRetriever.G, self.__current_day)
            self.update_new_covid_cases()
            self.__current_day += 1
            
            total_infected = 0
            for node in self.__dataRetriever.G.nodes:
                total_infected += self.__is_infected(node)

            print("There are " + str(total_infected) + " infected people.")

            print("Running covid force field")
            

    def __init__(self, data_retriever):
        self.__dataRetriever = data_retriever

if __name__ == "__main__":
    test_sim = SimulationFramework()
    test_sim.run_rimulation()
