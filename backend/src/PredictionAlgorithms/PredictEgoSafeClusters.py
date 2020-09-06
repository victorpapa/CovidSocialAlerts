import networkx as nx
import sys
sys.path.append(".")
from Data.DataRetriever import DataRetriever

class PredictEgoSafeClusters:

    __dataRetriever = None 
    __egoId = None
    __visited = None

    def clusterAnalysis(self):
        close_neighbors = self.__dataRetriever.G.adj[self.__egoId]
        neighbors_graph = nx.Graph()

        for close_neighbor in close_neighbors:
            neighbors_graph.add_node(close_neighbor, cumulative_field_infectiness = self.__dataRetriever.G.nodes[close_neighbor]["cumulative_field_infectiness"])

        for neighbor in close_neighbors:
            neighbor_neighbors = self.__dataRetriever.G.adj[neighbor]
            edges_to_add = [[neighbor, n] for n in neighbor_neighbors if n in close_neighbors]
            neighbors_graph.add_edges_from(edges_to_add)

        ccs = nx.biconnected_components(neighbors_graph)

        infectinesses= []

        for cc in ccs:
            max_infecti = 0

            curr_infectiness = 0

            infectiness = tuple()

            for node in cc:
                curr_infectiness += neighbors_graph.nodes[node]["cumulative_field_infectiness"]
                infectiness += (node,)
                
            curr_infectiness /= len(cc)

            infectiness += (curr_infectiness,)

            infectinesses += [infectiness]
            
        
        return infectinesses

    def predict(self):
        self.__clusterAnalysis()

    def __init__(self, egoId, dataRetriever):
        self.__egoId = egoId
        self.__dataRetriever = dataRetriever

if __name__ == "__main__":
    dataRetriever = DataRetriever()
    test = PredictEgoSafeClusters("ROM, SPACEKNIGHT", dataRetriever)
    test.clusterAnalysis()