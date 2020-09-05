from typing import List, Dict

class DataRetriever:

    # Obtain the list of all user_ids
    def get_users(self) -> List[int]:
        return

    # For a certain user, obtain the list of user_ids connected to him
    def get_users_connected_to(self, user_id: int) -> List[int]:
        return

    # Obtain a list of all the location_ids
    def get_locations(self) -> List[int]:
        return

    # Obtain all the user_ids that live in a certain location_id
    def get_users_at_location(self, location_id: int) -> List[int]:
        return

    # For a certain user_id, obtain the other user_ids that live in the same location_id
    def get_neighbours(self, user_id: int) -> List[int]:
        return

    # Obtain a list of all the work location_ids
    def get_work_locations(self) -> List[int]:
        return

    # Obtain all the user_ids that work in a certain location_id
    def get_users_working_at(self, work_location_id: int) -> List[int]:
        return

    # For a certain user_id, obtain the other user_ids that work in the same location_id
    def get_coworkers(self, user_id: int) -> List[int]:
        return

    # For a pair of user_ids, obtain the dictionary of labels for the edge between them (empty dict if not existent)
    def get_edge_labels_between(self, user_id1 : int, userid2 : int) -> Dict[str, int]:
        return
