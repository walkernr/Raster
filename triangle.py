# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 00:42:41 2013

@author: Nick Walker
"""

from RasterV1_2 import *
import fileinput
import sys

width = 512
height = 512

black = (0, 0, 0)

lines = Raster(width, height)

n = 0

for y in range(lines.getHeight()):
    for x in range(lines.getWidth()):
        lines.fillColor(x, y, black)

for line in fileinput.input():
    line = str(line)
    line = line.replace('\t', ' ')
    line = line.rstrip('\n')
    line = line.split(' ')
    if line[0] == 'c':
        r = int(float(line[1])*255.)
        g = int(float(line[2])*255.)
        b = int(float(line[3])*255.)
        lines.setCurrent((r,g,b))
    if line[0] == 'l':
        x0 = int(float(line[1]))
        y0 = int(float(line[2]))
        x1 = int(float(line[3]))
        y1 = int(float(line[4]))
        lines.drawLine(x0, y0, x1, y1, lines.getCurrent())
    if line[0] == 't':
        x0 = int(float(line[1]))
        y0 = int(float(line[2]))
        x1 = int(float(line[3]))
        y1 = int(float(line[4]))
        x2 = int(float(line[5]))
        y2 = int(float(line[6]))
        lines.drawTriangle(x0, y0, x1, y1, x2, y2, lines.getCurrent())

lines.dumpPPM('P6')