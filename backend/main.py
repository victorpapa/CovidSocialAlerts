from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
def read_clusters(user_id: int):
    return {
        "user-id": user_id,
        "clusters": [
            {
                "friends": [3, 4, 123],
                "risk": 1,
            },
            {
                "friends": [5, 10, 999],
                "risk": 0.6,
            },
            {
                "friends": [1234234, 124, 564573545, 354, 654, 7356, 756478, 876],
                "risk": 0.1,
            }
        ],
    }

@app.get("/risk/{user_id}")
def read_user_risk(user_id: int):
    return {
        "user-id": user_id,
        "risk": 0.63,
    }
