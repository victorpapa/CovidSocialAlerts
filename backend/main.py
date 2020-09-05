from fastapi import FastAPI
app = FastAPI()

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
def read_likelihood(user_id: int):
    return {
        "user-id": user_id,
        "risk": 0.63,
    }
