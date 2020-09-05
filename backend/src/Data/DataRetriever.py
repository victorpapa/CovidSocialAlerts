import os
import networkx as nx
import logging

class DataRetriever:

    social_network_file_name = None
    G = None
    social_network_file = None
    res_folder = None
    dataset = None
    dataset_folder = None
    backend_folder = None

    def __setup_logs(self):
        self.backend_folder = os.path.join(os.getcwd(), "..")
        log_folder_name = "log"
        if log_folder_name not in os.listdir(self.backend_folder):
            curr_dir = os.getcwd()
            os.chdir(os.path.join(self.backend_folder))
            os.makedirs(log_folder_name)
            os.chdir(curr_dir)

        log_folder = os.path.join(self.backend_folder, log_folder_name)
        log_file_name = "log.txt"
        if log_file_name not in os.listdir(log_folder):
            open(os.path.join(log_folder, log_file_name), "w+")

        logging.basicConfig(filename=os.path.join(log_folder, log_file_name), level=logging.DEBUG)

    def __init__(self):

        self.__setup_logs()

        self.res_folder = os.path.join(self.backend_folder, "res")
        self.social_network_file_name = os.path.join(self.res_folder, "infectinessHeroes", "hero-network.csv")
        self.social_network_file = open(self.social_network_file_name, "r")
        # self.dataset = "facebook"
        # self.dataset_folder = os.path.join(self.res_folder, self.dataset)

        self.__generate_graph()

    def __add_nodes_and_edges(self):

        for line in self.social_network_file:
            if "\"" not in line:
                continue
            
            ids = line.split("\"")

            # if len(ids) != 2:
            #     print("Invalid edge format: " + str(ids))
            #     exit()
            
            ids = [ids[1], ids[3]]
            
            self.G.add_nodes_from(ids, last_infection_time = -100,
                                       location = -1,
                                       work_location = -1)
            self.G.add_edge(ids[0], ids[1], co_worker = False)

    def __get_users_with_egos(self):
        user_set = set()
        for file_name in os.listdir(self.dataset_folder):
            user_set.add(int(file_name.split(".")[0]))

        return user_set

    def __get_featnames_for_user_ego(self, user_id):
        featnames = {}

        featnames_file_name = os.path.join(self.dataset_folder, str(user_id) + ".featnames")
        featnames_file = open(featnames_file_name, "r")

        for feature in featnames_file:
            if "work" in feature and "location" in feature:
                featnames[int(feature.split()[0]) + 1] = ("work_location", int(feature.split()[-1]))
            elif "location" in feature:
                featnames[int(feature.split()[0]) + 1] = ("location", int(feature.split()[-1]))

        return featnames


    def __set_metadata_for_user_ego(self, ego_user_id, featnames):
        
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

    def __set_co_worker_metadata(self):
        for user_id1 in self.G.nodes:
            for user_id2 in self.G.neighbors(user_id1):
                if self.G.nodes[user_id1]["work_location"] == self.G.nodes[user_id2]["work_location"] and                            self.G.nodes[user_id1]["work_location"] != -1:
                    self.G.edges[user_id1, user_id2]["co_worker"] = True

    def __add_nodes_and_edges_metadata(self):
        list_of_users_with_egos = self.__get_users_with_egos()

        for user_id in list_of_users_with_egos:
            featnames = self.__get_featnames_for_user_ego(user_id)
            self.__set_metadata_for_user_ego(user_id, featnames)

        self.__set_co_worker_metadata()

    def __generate_graph(self):
        self.G = nx.Graph()

        self.__add_nodes_and_edges()
        # self.__add_nodes_and_edges_metadata()

    def log_graph(self):
        for node in self.G.nodes.data():
            logging.info(node)
        
        for edge in self.G.edges.data():
            logging.info(edge)

    def graph(self):
        return self.G

if __name__ == "__main__":
    dataRetriever = DataRetriever()
    dataRetriever.log_graph()
    
