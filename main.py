import wander, animal_tracking
import concurrent.futures
import sys
import os

home = (51.4235505546458, -2.67083644866943)  # Fenswood
def roam_and_check(url):
	with concurrent.futures.ProcessPoolExecutor() as executor:
		  # Submit process 1
		future = executor.submit(animal_tracking.find_zebra)
		  # Start process 2
		wander.start_roaming(future, url)

if __name__ == '__main__':
	try:
		IP_RC = "192.168.1.4"
		url = f"http://{IP_RC}:8080"
		roam_and_check(url)
	except KeyboardInterrupt:
		print('Interrupted')
		#wander.Path_planning.requestSendStick(url)
		try:
			sys.exit(130)
		except SystemExit:
			os._exit(130)