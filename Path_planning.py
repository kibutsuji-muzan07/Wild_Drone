# IMPORTS
import requests
import ast
import pymap3d
import math
import sys
import os
import time

# CONSTANTS

# Aircraft state endpoints suffixes
# GETTER
EP_BASE = "/"
EP_SPEED = "/aircraft/speed"
EP_HEADING = "/aircraft/heading"
EP_ATTITUDE = "/aircraft/attitude"
EP_LOCATION = "/aircraft/location"
EP_GIMBAL_ATTITUDE = "/aircraft/gimbalAttitude"
EP_ALL_STATES = "/aircraft/allStates"

# SETTER
# expects a sting formated as: "<leftX>,<leftY>,<rightX>,<rightY>"
EP_STICK = "/send/stick"

# P-CONROLLER
CTRL_THRESH_HEAD = 5  # degrees
CTRL_THRESH_ALT = 0.5  # meters
CTRL_THRESH_X = 0.5  # meters
CTRL_THRESH_Y = 0.5  # meters

CTRL_GAIN_HEAD = 1/200
CTRL_GAIN_ALT = 0.05  # 0.1
CTRL_GAIN_X = 0.05  # 0.03
CTRL_GAIN_Y = 0.05  # 0.03

# FUNCTIONS


def requestGet(baseUrl, endPoint, verbose=False):
	response = requests.get(baseUrl + endPoint)
	if verbose:
		print("EP : " + endPoint + "\t" + str(response.content, encoding="utf-8"))
	return response


def requestAllStates(baseUrl, verbose=False):
	response = requestGet(baseUrl, EP_ALL_STATES, verbose)
	states = ast.literal_eval(response.content.decode(
	    'utf-8'))  # TODO: probably very unsafe!!!
	return states


def requestSend(baseUrl, endPoint, data, verbose=False):
	response = requests.post(baseUrl + endPoint, str(data))
	if verbose:
		print("EP : " + endPoint + "\t" + str(response.content, encoding="utf-8"))
	return response


def requestSendStick(baseUrl, leftX=0, leftY=0, rightX=0, rightY=0):
	# Saturate values such that they are in [-1;1]
	s = 0.3
	leftX = max(-s, min(s, leftX))
	leftY = max(-s, min(s, leftY))
	rightX = max(-s, min(s, rightX))
	rightY = max(-s, min(s, rightY))
	rep = requestSend(baseUrl, EP_STICK,
	                  f"{leftX:.4f},{leftY:.4f},{rightX:.4f},{rightY:.4f}")
	return rep


def main(url, dest_lat, dest_lon, dest_alt=20):
	requestGet(url, EP_BASE, True)
	requestSendStick(url)
    # Square at fenswood, right hand turn, altitude of waypoint to the south higher, looking about 45 deg to left
	trajectory = {"lat": dest_lat, "lon": dest_lon, "alt": dest_alt, "head": 0}

	# while True:
	# 	for wp in trajectory:
	# 		print(f"Going to wp : {wp}")
 	oldX = 0
    oldY=0
    oldZ=0
    oldH=0
    kDx=0.1
    kDy=0.1
    kDz=0.07
    kDh=1/200
    
    now=0
    lastT=0
	while True:
		# Get current state
		states = requestAllStates(url)
        # Computer error
		(errEast, errNorth, errUp) = pymap3d.geodetic2enu(
            trajectory["lat"], trajectory["lon"], trajectory["alt"],
            states["location"]["latitude"], states["location"]["longitude"], states["location"]["altitude"])
		distToWp = math.hypot(errEast, errNorth)
		bearingToWp = math.atan2(errEast, errNorth)
		errX =  -distToWp*math.cos(bearingToWp + math.pi/2 - states["heading"]/180.*math.pi)
		errY =  distToWp*math.sin(bearingToWp + math.pi/2 - states["heading"]/180.*math.pi)
		errAlt = errUp
<<<<<<< HEAD
		errHead = trajectory["head"] - states["heading"]

=======
		errHead = trajectory["head"] - trajectory["heading"]
  		dX = errX-oldX
    		dY = errY-oldY
    		dZ = errAlt-oldZ
    		dH = oldH-errHead
    		oldX = errX
        	oldY = errY
        	oldZ = errAlt
        	oldH = errHead
>>>>>>> 9aaaecae566a9e1cd3d7a3bcef83e26938f0bbac

        # Send control command
        	cmdBodyX = errX *CTRL_GAIN_X + kDx * dX
        	cmdBodyY = errY *CTRL_GAIN_Y + kDy * dY
        	cmdAlt = errAlt *CTRL_GAIN_ALT + kDz * dZ
        	cmdHead = errHead *CTRL_GAIN_HEAD + kDh * dH
        	print(now-lastT)
        	lastT=millis
			requestSendStick(url, cmdHead, cmdAlt, cmdBodyX, cmdBodyY)

        # Assess if waypoint reached
		if abs(errX) < CTRL_THRESH_X and abs(errY) < CTRL_THRESH_Y and abs(errAlt) < CTRL_THRESH_ALT and abs(errHead) < CTRL_THRESH_HEAD:
			requestSendStick(url)
			break
		
if __name__ == '__main__':
	try:
		IP_RC = "192.168.1.4"
		url = f"http://{IP_RC}:8080"
		main(url, dest_lat=51.7235413, dest_lon= -2.7708488)
	except KeyboardInterrupt:
		print('Interrupted')
		requestSendStick(url)
		try:
			sys.exit(130)
		except SystemExit:
			os._exit(130)