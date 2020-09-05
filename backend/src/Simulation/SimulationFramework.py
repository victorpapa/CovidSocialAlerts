from Data.DataRetriever import DataRetriever
import random

class SimulationFramework:

    __current_day = 0
    __dataRetriever = None

    def __infectiness(self, last_infection_time):
        return self.__current_day - last_infection_time < 10

    def __update_new_covid_cases(self):
        nodes = __dataRetriever.G.nodes()

        for node in nodes:
            if self.__current_day == 0:
                node_gets_infected = random.random() < 0.5
            else:
                node_gets_infected = self.__infectiness(node["last_infection_time"])

            if node_gets_infected == True:
                node["last_infection_time"] = self.__current_day
                
    def run_rimulation(self):

        self.__update_new_covid_cases()

        while True:
            
            self.force_field(self.__dataRetriever.G, self.__current_day)
            self.update_new_covid_cases()
            self.current_day += 1

    def __init__(self):
        self.__dataRetriever = DataRetriever()
