## IMPORTS
import Path_planning
import concurrent.futures

def start_roaming(future, url):
    trajectory = [{"lat": 51.4241794,"lon": -2.6696670, "alt": 35, "head":0},
                {"lat": 51.4227477,"lon": -2.6690555, "alt": 35, "head":0},
                {"lat": 51.4232227,"lon": -2.6720488, "alt": 35, "head":0},
                {"lat": 51.4215636,"lon": -2.6708579, "alt": 35, "head":0},
                {"lat": 51.4222460,"lon": -2.6700747, "alt": 35, "head":0},
                {"lat": 51.4240590,"lon": -2.6702893, "alt": 35, "head":0}]

    while True:
        try:
            # Check if process 1 has finished (exception if cancelled)
            result = future.result(timeout=0.1)  # Check with a timeout
            break  # Exit the loop when process 1 finishes
        except concurrent.futures.TimeoutError:
            # Continue the loop if process 1 hasn't finished yet
            for wp in trajectory:
                Path_planning.move(future, url, wp["lat"], wp["lon"], wp["alt"])
        except concurrent.futures.CancelledError:
            print("Finding zebra stopped (detection cancelled)")
            break  # Exit the loop on cancellation
