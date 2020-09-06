import sys
sys.path.append('.')

import networkx as nx

from Data.DataRetriever import DataRetriever
# from Simulation.SimulationFramework import SimulationFramework
# from PredictEgoSafeClusters import PredictEgoSafeClusters

coefficients = {
    0: 1,
    1: 0.7,
    2: 0.3,
    3: 0.1,
}

def reset_risk(G):
    for node in G.nodes():
        G.nodes[node]["cumulative_field_infectiness"] = 0

def force_field(G, day):
    reset_risk(G)
    for node in G.nodes():
        node_infectiness = infectiness(day - G.nodes[node]["last_infection_time"]) 
        #print("Node last infected at {} with infectiness {}".format(G.nodes[node]["last_infection_time"], node_infectiness))
        if node_infectiness > 0:
            # print("computing force field diffusion")
            for level in range(1, 4):
                level_descendents = nx.descendants_at_distance(G, node, level)
                # print("{} descendents at level {}".format(len(level_descendents), level))
                for descendent in level_descendents:
                    G.nodes[descendent]["cumulative_field_infectiness"] = max(
                        G.nodes[descendent]["cumulative_field_infectiness"],
                        node_infectiness * coefficients[level]
                    )

    # print("Infectiness incomming")
    # for node in G.nodes():
    #     print(G.nodes[node]["cumulative_field_infectiness"])

# Should probably look at other modes of infectiness
def infectiness(days_since_diagnosis: int) -> float:
    if days_since_diagnosis < 5:
        return 1
    elif days_since_diagnosis < 8:
        return 0.8
    elif days_since_diagnosis < 10:
        return 0.6
    elif days_since_diagnosis < 14:
        return 0.7
    elif days_since_diagnosis < 20:
        return 0.5
    else: return max((42 - days_since_diagnosis) / 14, 0)

# if __name__ == "__main__":
#     dr = DataRetriever()

#     sf = SimulationFramework(dr)
#     sf.update_new_covid_cases()

#     force_field(dr.graph(), 0)
#     #dr.log_graph()

#     test = PredictEgoSafeClusters("ROM, SPACEKNIGHT", dr)
#     test.clusterAnalysis()
