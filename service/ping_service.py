from fastapi import FastAPI, HTTPException
from pythonping import ping
from pydantic import BaseModel
import json
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINTS_FILE = os.path.join(BASE_DIR, "endpoints.json")

class PingRequest(BaseModel):
    target: str
    count: int = 5
    timeout: int = 1
    interval: float = 0.2
    size: int = 32

class MultiTargetPingRequest(BaseModel):
    targets: list[str]
    count: int = 5
    timeout: int = 1
    interval: float = 0.2
    size: int = 32

class MultiRegionPingRequest(BaseModel):
    regions: list[str]
    count: int = 5
    timeout: int = 1
    interval: float = 0.2
    size: int = 32

def load_endpoints():
    with open(ENDPOINTS_FILE) as f:
        return json.load(f)

def ping_target(target: str, count: int, timeout: int, interval: float, size: int):
    responses = ping(target, count=count, timeout=timeout, interval=interval, size=size)
    latencies = [resp.time_elapsed_ms for resp in responses if resp.success]
    failures = count - len(latencies)

    if latencies:
        return {
            "target": target,
            "min": f"{round(min(latencies), 2)} ms",
            "max": f"{round(max(latencies), 2)} ms",
            "avg": f"{round(sum(latencies)/len(latencies), 2)} ms",
            "packet loss": f"{round((failures/count) * 100, 1)}%",
            "success": True
        }
    else:
        return {
            "target": target,
            "min": None,
            "max": None,
            "avg": None,
            "packet loss": "100.0%",
            "success": False
        }
        
@app.post("/ping/targets")
def ping_multiple_targets(request : MultiTargetPingRequest):
    results = []

    for target in request.targets:
        result = ping_target(target, request.count, request.timeout, request.interval, request.size)
        results.append(result)

    return results

@app.post("/ping/regions")
def ping_multiple_regions(request: MultiRegionPingRequest):
    data = load_endpoints()
    results = {}

    for region in request.regions:
        if region not in data:
            raise HTTPException(status_code=404, detail=f"Region '{region}' not found")

        region_results = []
        for target in data[region]:
            try:
                result = ping_target(target, request.count, request.timeout, request.interval, request.size)
            except Exception as e:
                result = {
                    "target": target,
                    "success": False,
                    "error": str(e)
                }
            region_results.append(result)
        
        results[region] = region_results

    return results

@app.post("/ping/{target}")
def ping_target_endpoint(target: str):
    result = ping_target(target, 5, 1, 0.2, 32)
    return result


@app.get("/ping")
def ping_endpoints():
    regions = load_endpoints()
    results = {}

    for region, endpoints in regions.items():
        region_results = []
        for target in endpoints:
            result = ping_target(target, 5, 1, 0.2, 32)
            region_results.append(result)
        results[region] = region_results

    return results

