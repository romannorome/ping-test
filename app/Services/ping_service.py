from pythonping import ping
import json

def ping_target(target, count, timeout, interval, size):
    responses = ping(target, count=count, timeout=timeout, interval=interval, size=size)
    latencies = [resp.time_elapsed_ms for resp in responses if resp.success]
    failures = count - len(latencies)

    if latencies:
        return{
            "target": target,
            "min": min(latencies),
            "max": max(latencies),
            "avg": sum(latencies)/len(latencies),
            "packet loss": (failures/count) * 100,
            "success": True
        }
    else:
        return{
            "target": target,
            "success": False,
            "packet loss": 100
        }

def main():
    with open("endpoints.json") as f:
        regions = json.load(f)
    
    for region, endpoints in regions.items():
        print(f"\n== {region} ==")
        for target in endpoints:
            result = ping_target(target, 5, 1, 0.2, 32)

            if result["success"]:
                print(f"{target:<16} Min: {result['min']:.2f} ms  Max: {result['max']:.2f} ms  Avg: {result['avg']:.2f} ms  Loss: {result['packet loss']:.1f}%")
                
            else:
                print(f"{target:<16} All pings failed.  Loss: {result['packet loss']:.1f}%")


if __name__ == "__main__":
    main()