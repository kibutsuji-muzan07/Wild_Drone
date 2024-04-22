import wander, animal_tracking, approach_object
#import locate_coordinate, take_snaps
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
		IP_RC = "192.168.1.2"
		url = f"http://{IP_RC}:8080"
		#initialize
		roam_and_check(url)
		#todo
		#lat,lon,alt = locate_coordinate()
		#approach_object.approach(url, lat, lon, alt)
		#flag = take_snaps() # return something, indicating taking snaps are done
		approach_object.return_to_launch(url, home)
	except KeyboardInterrupt:
		print('Interrupted')
		try:
			sys.exit(130)
		except SystemExit:
			os._exit(130)