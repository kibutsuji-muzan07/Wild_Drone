from drone_movement import *
import concurrent.futures
import pymap3d
import math

def move(future, url, dest_lat =0, dest_lon =0, dest_alt = 20, head = 0):
	requestGet(url, EP_BASE, True)
	requestSendStick(url)
    # Square at fenswood, right hand turn, altitude of waypoint to the south higher, looking about 45 deg to left
	#trajectory = {"lat": dest_lat,"lon": dest_lon, "alt": dest_alt, "head":0}

	# while True:
	# 	for wp in trajectory:
	# 		print(f"Going to wp : {wp}")
	while True:
		try:
			# Check if process 1 has finished (exception if cancelled)
			result = future.result(timeout=0.1)  # Check with a timeout
			print(f"Process 1: Zebra found! ({result})")
			requestSendStick(url)
			break  # Exit the loop when process 1 finishes
		except concurrent.futures.TimeoutError:
			# Continue the loop if detection hasn't finished yet
			# Get current state
			states = requestAllStates(url)
			# Computer error
			(errEast, errNorth, errUp) = pymap3d.geodetic2enu(
				dest_lat, dest_lon, dest_alt,
				states["location"]["latitude"], states["location"]["longitude"], states["location"]["altitude"]
				)
			distToWp = math.hypot(errEast, errNorth)
			bearingToWp = math.atan2(errEast, errNorth)
			errX =  -distToWp*math.cos(bearingToWp + math.pi/2 - states["heading"]/180.*math.pi)
			errY =  distToWp*math.sin(bearingToWp + math.pi/2 - states["heading"]/180.*math.pi)
			errAlt = errUp
			errHead = head - states["heading"]

			#Send control command
			cmdBodyX = errX*CTRL_GAIN_X
			cmdBodyY = errY*CTRL_GAIN_Y
			cmdAlt = errAlt*CTRL_GAIN_ALT
			cmdHead = errHead*CTRL_GAIN_HEAD
			requestSendStick(url, cmdHead, cmdAlt, cmdBodyX, cmdBodyY)

			# Assess if waypoint reached
			if abs(errX) < CTRL_THRESH_X and abs(errY) < CTRL_THRESH_Y and abs(errAlt) < CTRL_THRESH_ALT and abs(errHead) < CTRL_THRESH_HEAD:
				requestSendStick(url)
				break
			print("Process 2: Waiting for detection...")
		except concurrent.futures.CancelledError:
			print("Finding zebra stopped (detection cancelled)")
			break  # Exit the loop on cancellation