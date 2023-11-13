from pydantic import BaseModel


# 2. Class which describes two teams
class Match(BaseModel):
    team1: object
    team2: object
    toss_winner: object
    toss_decision: object
    city: object
    venue: object
