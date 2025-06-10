from fastapi import APIRouter, HTTPException, Request, Response
from service.ping_service import ping_target

import json

router = APIRouter()

@router.get("/regions")
def get_regions():
    with open('endpoints.json') as file:
        data = json.load(file)

    return list(data.keys())

@router.get("/regions/details")
def get_regions():
    with open('endpoints.json') as file:
        data = json.load(file)

    return data

