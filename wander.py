## IMPORTS
import Path_planning
import concurrent.futures

def start_roaming(future, url):
    trajectory = [{"lat": 51.4237513,"lon": -2.6695061, "alt": 25, "head":0},
                {"lat": 51.4227477,"lon": -2.6690555, "alt": 25, "head":0},
                {"lat": 51.4230555,"lon": -2.6716304, "alt": 25, "head":0},
                {"lat": 51.4218245,"lon": -2.6704931, "alt": 25, "head":0},
                {"lat": 51.422246,"lon": -2.6700747, "alt": 25, "head":0},
                {"lat": 51.423671,"lon": -2.670064, "alt": 25, "head":0}]

    while True:
        # try:
        #     # Check if process 1 has finished (exception if cancelled)
        #     result = future.result(timeout=0.1)  # Check with a timeout
        #     break
        # except concurrent.futures.TimeoutError:
        #     # Continue the loop if process 1 hasn't finished yet
        #     for wp in trajectory:
        #         info, height = Path_planning.move(future, url, wp["lat"], wp["lon"], wp["alt"])
        # except concurrent.futures.CancelledError:
        #     print("Finding zebra stopped (detection cancelled)")
        #     break  # Exit the loop on cancellation

        for wp in trajectory:
            info, height = Path_planning.move(future, url, wp["lat"], wp["lon"], wp["alt"])
            if info is not None:
                return info, height
            else:
                continue