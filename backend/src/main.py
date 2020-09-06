from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading

import sys
sys.path.append('.')

from Data.DataRetriever import DataRetriever
from Simulation.SimulationFramework import SimulationFramework

dr = DataRetriever()
sf = SimulationFramework(dr)


x = threading.Thread(target=sf.run_simulation)
x.start()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    # I think this should dump out the current status of the entire graph
    return {"welcome": "The api is online"}

@app.get("/clusters/{user_id}")
def read_clusters(user_id: str):
    clusters = sf.cluster_analysis(user_id)
    formated_clusters = []
    for cluster in clusters:
        formated_clusters.append({
            "friends": list(cluster[:-1]),
            "risk": cluster[-1]
        })
    return {
        "user-id": user_id,
        "clusters": formated_clusters,
    }

@app.get("/risk/{user_id}")
def read_user_risk(user_id: str):
    infectiness = dr.graph().nodes[user_id]["cumulative_field_infectiness"]
    return {
        "user-id": user_id,
        "risk": infectiness,
    }

@app.get("/gotit/{user_id}")
def covid_a_user(user_id: str):
    sf.set_last_infection_time_to_current_day(user_id)
    return {}

@app.get("/dayssince/{user_id}")
def get_days_since(user_id: str):
    return sf.current_day - dr.G.nodes[user_id]["last_infection_time"]
