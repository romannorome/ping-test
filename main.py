from fastapi import FastAPI, HTTPException, Request, Response
import json
from app import Services
from app.Services.ping_service import ping_target

app = FastAPI()

@app.get("/regions")
def get_regions():
    with open('endpoints.json') as file:
        data = json.load(file)

    return list(data.keys())

@app.get("/ping/{target}")
def ping(target:str):
    return ping_target(target, 5, 1, 0.2, 32 )
