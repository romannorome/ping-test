from fastapi import FastAPI, HTTPException, Request, Response
import json
from app.Controllers import ping_controller

app = FastAPI()

app.include_router(ping_controller.router)


