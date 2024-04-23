import math
import sys
import time


def calculate_values(a1, h, x1, y1, z,dy):

    x=x1-320
    y=y1-240
    H=2000
    d1 = 5
    angle1 = math.radians(41)
    d2 = 2.5 / math.tan(angle1)
    d3 = y * d1 / z
    d4 = x * d1 / z
    a2 = math.atan(d3 / d2)
    angle2 = math.radians(a1)
    d5 = h * math.tan(angle2 + a2)
    d6 = math.sqrt(h ** 2 + d5 ** 2)
    d7 = math.sqrt(d3 ** 2 + d2 ** 2)
    d8 = d4 * d6 / d7
    d9 = math.sqrt(d2 ** 2 + d3 ** 2 + d4 ** 2)
    a3 = math.atan(d8 / d5)
    d10 = math.sqrt(h ** 2 + d5 ** 2 + d8 ** 2)
    a4 = -math.sin(h / d10)
    D = d9 * (H - dy) / dy

    return d9, a3, a4

def get_animal_pos(info, height):
#a1 is the camera pitch angle
#h is the altitude
#x and y are the coordinates of the animal in the photo
#z is the diagonal length of the photo
#The length unit of the input variable is millimeter
# the angle unit of the input variable is degree.
    xres= info["xres"]
    yres = info["yres"]
    x1= info["x1"]
    x2=info["x2"]
    y1=info["y1"]
    y2=info["y2"]

    a1 = 45
    h = height
    x = (x1+x2)/2
# x = pixel x - 320
    y = (y1+y2)/2
# y = -pixel y + 240
    z = math.sqrt((xres**2)+(yres**2))
    P = y2-y1
# P is the pixel height in screen
    H = 600
#H is the real zebra height
    P1 = 5 * P / z

    d9, a3, a4 = calculate_values(a1, h, x, y, z,P)
    D = d9 * (H - P1) / P1
    dhrad=a3
    dhdeg=(a3*180)/math.pi
    dX= (math.cos(a3)*(D-2000))/1000
    dY= (math.sin(a3)*(D-2000))/1000
    dAlt= h*(math.tan(a4+45))
    
    #1183744 + 518400=1702144= 1305
#     print("yaw angle:", a3,)
# # If bigger than 0, it indicates that the nose needs to point rightwards
#     print("pitch angle:", a4,)
# # If bigger than 0, it indicates that the nose needs to point upwards
#     print("distance:", D/1000)
    
    # print("X dist to animal:", dX, "\ny dist to animal: ",dY, "\nheading change: ", dhrad,"|", dhdeg)
    return dX, dY, dAlt, dhdeg
#The length unit of the output variable is meter
#The output angle unit is radians
