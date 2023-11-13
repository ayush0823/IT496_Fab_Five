# import library
import uvicorn
from fastapi import FastAPI
from DataModel import Match
import numpy as np
import pickle
import pandas as pd

# create the app object
app = FastAPI()
pickle_model = open("classifier.pkl", "rb")
classifier = pickle.load(pickle_model)

# Load the model and encoding information
with open("classifier.pkl", "rb") as file:
    loaded_data = pickle.load(file)

model = loaded_data["model"]
encoding_info = loaded_data["encoding_info"]


# default route
@app.get("/")
def index():
    return {"message": "Hello IDM Students"}


# default route
@app.get("/api-demo")
def index():
    return {"message": "This is demo API"}


# Prediction Function, return the predicted result in JSON
@app.post("/predict")
def predict(data: Match):
    # convert data obj to dictionary
    data = dict(data)
    team1 = data["team1"]
    team2 = data["team2"]
    toss_winner = data["toss_winner"]
    toss_decision = data["toss_decision"]
    city = data["city"]
    venue = data["venue"]

    # encode team1
    team_map = encoding_info["team_map"]
    # print(team_map)
    team1_code = team_map.get(team1, -1)  # Use -1 if team is not in the map
    team2_code = team_map.get(team2, -1)  # Use -1 if team is not in the map
    toss_winner_code = team_map.get(toss_winner, -1)

    # encode toss_decision as 1 if fielding, 0 if batting
    toss_decision_field = 1 if toss_decision == "field" else 0

    # encode city
    city_map = encoding_info["city_encoding_categories"]
    # Assuming city is a variable containing the city name
    try:
        city_code = city_map.get_loc(city)
    except KeyError:
        city_code = -1  # Use -1 if city is not in the categories

    # encode venue
    venue_map = encoding_info["venue_encoding_categories"]
    # print(venue_map)
    try:
        venue_code = venue_map.get_loc(venue)
    except KeyError:
        venue_code = -1

    prediction = model.predict(
        [
            [
                0,
                0,
                toss_winner_code,
                venue_code,
                city_code,
                team1_code,
                team2_code,
                toss_decision_field,
            ]
        ]
    )[0]

    # print(prediction)
    if prediction == 1:
        return {"prediction": team1}
    else:
        return {"prediction": team2}
    # return {"prediction": prediction}


# Run the API with uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


# Command to run API server
# python -m uvicorn main:app --reload
