import sys
sys.path.append('.')
from Data.DataRetriever import DataRetriever
from PredictionAlgorithms.force_field import force_field
from PredictionAlgorithms.PredictEgoSafeClusters import PredictEgoSafeClusters
import random
import time

class SimulationFramework:

    current_day = 0
    __dataRetriever = None

    def __is_infected(self, node):
        return self.current_day - self.__dataRetriever.G.nodes[node]["last_infection_time"] < 10

    def __probability_of_infection(self, node):
        my_sum = 0

        for neighbor in self.__dataRetriever.G.neighbors(node):
            is_already_infected = self.__is_infected(neighbor)
            my_sum += is_already_infected

        return my_sum / (len(list(self.__dataRetriever.G.neighbors(node))) * 5)

    def update_new_covid_cases(self):

        for node in self.__dataRetriever.G.nodes:

            if self.current_day == 0:
                node_gets_infected = random.random() < 0.001
            else:
                is_already_infected = self.__is_infected(node)

                if not is_already_infected:
                    node_gets_infected = random.random() < self.__probability_of_infection(node)
                else:
                    continue

            if node_gets_infected == True:
                self.__dataRetriever.G.nodes[node]["last_infection_time"] = self.current_day

    def run_simulation(self):

        self.update_new_covid_cases()

        while True:
            # self.force_field(self.__dataRetriever.G, self.current_day)
            self.update_new_covid_cases()
            self.current_day += 1

            total_infected = 0
            for node in self.__dataRetriever.G.nodes:
                total_infected += self.__is_infected(node)

            # print("There are " + str(total_infected) + " infected people.")

            # print("Running covid force field")
            force_field(self.__dataRetriever.graph(), self.current_day)
            time.sleep(5)


    def __init__(self, data_retriever):
        self.__dataRetriever = data_retriever

    def set_last_infection_time_to_current_day(self, user_id):
        self.__dataRetriever.G.nodes[user_id]["last_infection_time"] = self.current_day

    def cluster_analysis(self, userid):
        aux = PredictEgoSafeClusters(userid, self.__dataRetriever)
        return aux.clusterAnalysis()


if __name__ == "__main__":
    dr = DataRetriever()
    test_sim = SimulationFramework(dr)
    test_sim.run_simulation()
