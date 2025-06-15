## IMPORTS
import requests
import ast
from security import safe_requests

## CONSTANTS

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
EP_STICK = "/send/stick" # expects a sting formated as: "<leftX>,<leftY>,<rightX>,<rightY>"

# P-CONROLLER
CTRL_THRESH_HEAD = 5 # degrees
CTRL_THRESH_ALT = 0.5 # meters
CTRL_THRESH_X = 2.5 # meters
CTRL_THRESH_Y = 2.5 # meters

CTRL_GAIN_HEAD = 1/200
CTRL_GAIN_ALT = 0.1
CTRL_GAIN_X = 0.03
CTRL_GAIN_Y = 0.03

## FUNCTIONS
def requestGet(baseUrl, endPoint, verbose=False):
	response = safe_requests.get(baseUrl + endPoint)
	if verbose:
		print("EP : " + endPoint + "\t" + str(response.content, encoding="utf-8"))
	return response

def requestAllStates(baseUrl, verbose=False):
	response = requestGet(baseUrl, EP_ALL_STATES, verbose)
	states = ast.literal_eval(response.content.decode('utf-8')) # TODO: probably very unsafe!!!
	return states

def requestSend(baseUrl, endPoint, data, verbose=False):
	response = requests.post(baseUrl + endPoint, str(data))
	if verbose:
		print("EP : " + endPoint + "\t" + str(response.content, encoding="utf-8"))
	return response

def requestSendStick(baseUrl, leftX = 0, leftY = 0, rightX = 0, rightY = 0):
	# Saturate values such that they are in [-1;1]
	s = 0.1
	leftX = max(-s,min(s,leftX))
	leftY = max(-s,min(s,leftY))
	rightX = max(-s,min(s,rightX))
	rightY = max(-s,min(s,rightY))
	rep = requestSend(baseUrl, EP_STICK, f"{leftX:.4f},{leftY:.4f},{rightX:.4f},{rightY:.4f}")
	return rep
