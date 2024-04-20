from drone_movement import *
import pymap3d
import math

def approach(url, lat, lon, alt, head = 0):
    requestSendStick(url)
    while True:
        # Get current state
        states = requestAllStates(url)

        # Computer error
        (errEast, errNorth, errUp) = pymap3d.geodetic2enu(
            lat, lon, alt,
            states["location"]["latitude"], states["location"]["longitude"], states["location"]["altitude"]
            )
        distToWp = math.hypot(errEast, errNorth)
        bearingToWp = math.atan2(errEast, errNorth)
        errX =  -distToWp*math.cos(bearingToWp + math.pi/2 - states["heading"]/180.*math.pi)
        errY =  distToWp*math.sin(bearingToWp + math.pi/2 - states["heading"]/180.*math.pi)
        errAlt = errUp
        errHead = head - states["heading"]


        # Send control command
        cmdBodyX = errX*CTRL_GAIN_X
        cmdBodyY = errY*CTRL_GAIN_Y
        cmdAlt = errAlt*CTRL_GAIN_ALT
        cmdHead = errHead*CTRL_GAIN_HEAD
        requestSendStick(url, cmdHead, cmdAlt, cmdBodyX, cmdBodyY)

        # Assess if waypoint reached
        if abs(errX) < CTRL_THRESH_X and abs(errY) < CTRL_THRESH_Y and abs(errAlt) < CTRL_THRESH_ALT and abs(errHead) < CTRL_THRESH_HEAD:
            requestSendStick(url)
            break

def return_to_launch(url, home):
    approach(url, home[0], home[1], alt = 1)