from random import random

MAX_X_COORD = 1000.0
MAX_Y_COORD = 1000.0
MAX_R = 0
CIRCLE_COUNT = 10000

def dxf_circle(x, y, r):
    return "0\nCIRCLE\n8\n0\n10\n{x:.3f}\n20\n{y:.3f}\n40\n{r:.2f}\n".format(x=x, y=y, r=r)

with open("D:\\.temp\\circles.dxf", 'wt') as f:
    f.write("0\nSECTION\n2\nENTITIES\n")
    for i in range(CIRCLE_COUNT):
        f.write(dxf_circle(MAX_X_COORD*random(), MAX_Y_COORD*random(), MAX_R*random()))
    f.write("0\nENDSEC\n0\nEOF\n")