import numpy as np
from PIL import Image
import math
def checkIfEdge(x, y):
    if x - 1 < 0 or y - 1 < 0 or x + 1 >= 1001 or y + 1 >= 751:
        return True


def calculateD(x, y, data):
    A = data[x - 1][y - 1]
    B = data[x - 1][y]
    C = data[x - 1][y + 1]
    D = data[x][y - 1]
    E = data[x][y]
    F = data[x][y + 1]
    G = data[x + 1][y - 1]
    H = data[x + 1][y]
    I = data[x + 1][y + 1]

    dzdx = ((C + 2 * F + I) - (A + 2 * D + G)) / 8
    dzdy = ((G + 2 * H + I) - (A + 2 * B + C)) / 8

    return dzdx, dzdy


def calculateSlope(dzdx, dzdy):
    slope = max(math.atan(math.sqrt(dzdx ** 2 + dzdy ** 2)), 0)
    return slope


def getAspect(slope, dzdx, dzdy):
    aspect = 0

    if (slope > 0):
        aspect = (math.atan2(dzdy, -dzdx) + 2 * math.pi) % 2 * math.pi
    else:
        if (dzdy > 0):
            aspect = math.pi / 2
        elif (dzdy < 0):
            aspect = (3 * math.pi) / 2
    return aspect


def calculateShading(zenit, azimut, slope, aspect):
    shading = (math.cos(-zenit) * math.cos(slope)) + (math.cos(azimut - aspect) * math.sin(-zenit) * math.sin(slope))
    return shading


def HillShading(data, image, zenit, azimut, conv):
    xcounter = 0
    ycounter = 0
    for x in range(image.width):
        xcounter = xcounter + 1
        for y in range(image.height):
            ycounter = ycounter + 1
            if (checkIfEdge(y, x) != True):
                dzdx, dzdy = calculateD(y, x, data)
                slope = calculateSlope(dzdx, dzdy)
                aspect = getAspect(slope, dzdx, dzdy)
                shading = calculateShading(zenit, azimut, slope, aspect)
                image.putpixel((x, y), shading * 255)
    image.show()
    return conv


image = Image.open('test.tif')  # vhodna slika
converted = np.zeros((1001, 751))
print(converted)

data = np.asarray(image)

zenit = input()
azimut = input()

zenit = math.radians(int(zenit))
azimut = math.radians(int(azimut))

conv = HillShading(data, image, zenit, azimut, converted)
