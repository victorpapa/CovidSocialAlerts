import os
import networkx as nx
import sys
import logging
sys.path.append('..')

from Utils.TxtToCsvConverter import generate_social_network_csv

class DataRetriever:

    social_network_file_name = None
    G = None
    social_network_file = None
    res_folder = None
    dataset = None
    dataset_folder = None

    def __init__(self):
        log_folder = os.path.join(os.getcwd(), "..", "..", "log")
        log_file_name = "log.txt"
        if log_file_name not in os.listdir(log_folder):
            open(os.path.join(log_folder, log_file_name), "w+")

        logging.basicConfig(filename=os.path.join(log_folder, log_file_name), level=logging.DEBUG)
        self.res_folder = os.path.join(os.getcwd(), "..", "..", "res")
        self.social_network_file_name = os.path.join(self.res_folder, "facebook_combined.txt")
        self.social_network_file = open(self.social_network_file_name, "r")
        self.dataset = "facebook"
        self.dataset_folder = os.path.join(self.res_folder, self.dataset)

    def add_nodes_and_edges(self):

        for line in self.social_network_file:
            ids = line.split()

            if len(ids) != 2:
                print("Invalid edge format: " + str(ids))
                exit()
            
            ids = [int(id) for id in ids]
            
            self.G.add_nodes_from(ids, last_infection_time = -1,
                                       location = -1,
                                       work_location = -1)
            self.G.add_edge(ids[0], ids[1], co_worker = False)

    def _get_users_with_egos(self):
        user_set = set()
        for file_name in os.listdir(self.dataset_folder):
            user_set.add(int(file_name.split(".")[0]))

        return user_set

    def _get_featnames_for_user_ego(self, user_id):
        featnames = {}

        featnames_file_name = os.path.join(self.dataset_folder, str(user_id) + ".featnames")
        featnames_file = open(featnames_file_name, "r")

        for feature in featnames_file:
            if "work" in feature and "location" in feature:
                featnames[int(feature.split()[0]) + 1] = ("work_location", int(feature.split()[-1]))
            elif "location" in feature:
                featnames[int(feature.split()[0]) + 1] = ("location", int(feature.split()[-1]))

        return featnames


    def _set_metadata_for_user_ego(self, ego_user_id, featnames):
        
        egofeat_file_name = os.path.join(self.dataset_folder, str(ego_user_id) + ".egofeat")
        egofeat_file = open(egofeat_file_name, "r")

        for features in egofeat_file:
            features = features.split()
            current_user_id = ego_user_id

            for feat_key in featnames:
                if int(features[feat_key - 1]) == 1:
                    self.G.nodes[current_user_id][featnames[feat_key][0]] = featnames[feat_key][1]

        egofeat_file.close()

        feat_file_name = os.path.join(self.dataset_folder, str(ego_user_id) + ".feat")
        feat_file = open(feat_file_name, "r")

        for features in feat_file:
            features = features.split()
            current_user_id = int(features[0])

            for feat_key in featnames:
                if int(features[feat_key]) == 1:
                    self.G.nodes[current_user_id][featnames[feat_key][0]] = featnames[feat_key][1]

        feat_file.close()

    def _set_co_worker_metadata(self):
        for user_id1 in self.G.nodes:
            for user_id2 in self.G.neighbors(user_id1):
                if self.G.nodes[user_id1]["work_location"] == self.G.nodes[user_id2]["work_location"] and                self.G.nodes[user_id1]["work_location"] != -1:
                    self.G.edges[user_id1, user_id2]["co_worker"] = True

    def add_nodes_and_edges_metadata(self):
        list_of_users_with_egos = self._get_users_with_egos()

        for user_id in list_of_users_with_egos:
            featnames = self._get_featnames_for_user_ego(user_id)
            self._set_metadata_for_user_ego(user_id, featnames)

        self._set_co_worker_metadata()

    def generate_graph(self):
        self.G = nx.Graph()

        self.add_nodes_and_edges()
        self.add_nodes_and_edges_metadata()

    def log_graph(self):
        for node in self.G.nodes.data():
            logging.info(node)
        
        for edge in self.G.edges.data():
            logging.info(edge)

    def graph(self):
        return G

if __name__ == "__main__":
    dataRetriever = DataRetriever()
    dataRetriever.generate_graph()
    dataRetriever.log_graph()
    
