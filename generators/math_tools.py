import math

def findCircumcircleRadius(radius, sides):
    return radius / math.cos(math.pi/sides)

def findInscribedRadius(radius, sides):
    return radius * math.cos(math.pi/sides)