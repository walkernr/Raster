# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 19:59:42 2013

@author: Nick Walker
"""

import sys

class Raster:

    """Constructs a Raster"""
    def __init__(self, height, width):
        """ Initializes the Raster"""
        self._height = height
        self._width = width
        self._colors = []
        self._current = (0, 0, 0)
        for y in range(self._height):
            self._colors.append([])
            for x in range(self._width):
                self._colors[y].append((0, 0, 0))

    def fillColor(self, x, y, color):
        """Colors a Pixel"""
        self._colors[y][x] = color

    def exportPPM(self, name, type):
        """Uses the Image Data to Export a P6 PPM"""
        file = open(name + '.ppm', "wb")
        if type == 'P6':
	        file.write('P6' + ' ' + str(self.getWidth()) + ' ' + str(self.getHeight()) + ' ' + '255' + ' ')
	        for y in range(self.getHeight()):
	            for x in range(self.getWidth()):
	                file.write(self.convertColor(x, y))
	        file.close()
        if type == 'P3':
	        file.write('P3' + '\n' + str(self.getWidth()) + ' ' + str(self.getHeight()) + '\n' + '255' + '\n')
	        for y in range(self.getHeight()):
	            for x in range(self.getWidth()):
	                file.write(self.convertColorAscii(x, y) + '\t')
	            file.write('\n')
        file.close()

    def dumpPPM(self, type):
        """Uses the Image Data to Dump to Stdout"""
        if type == 'P6':
	        sys.stdout.write('P6' + ' ' + str(self.getWidth()) + ' ' + str(self.getHeight()) + ' ' + '255' + ' ')
	        for y in range(self.getHeight()):
	            for x in range(self.getWidth()):
	                sys.stdout.write(self.convertColor(x, y))
        if type == 'P3':
	        sys.stdout.write('P3' + '\n' + str(self.getWidth()) + ' ' + str(self.getHeight()) + '\n' + '255' + '\n')
	        for y in range(self.getHeight()):
	            for x in range(self.getWidth()):
	                sys.stdout.write(self.convertColorAscii(x, y) + '\t')
	            sys.stdout.write('\n')

    def getWidth(self):
        """Returns Image Width"""
        return self._width

    def getHeight(self):
        """Returns Image Height"""
        return self._height

    def convertColor(self, x, y):
        """Returns the Color"""
        r = chr(self._colors[x][y][0])
        g = chr(self._colors[x][y][1])
        b = chr(self._colors[x][y][2])
        return r + g + b

    def convertColorAscii(self, x, y):
        """Returns the Color"""
        r = str(self._colors[x][y][0])
        g = str(self._colors[x][y][1])
        b = str(self._colors[x][y][2])
        return r + ' ' + g + ' ' + b

    def getColor(self, x, y):
        """Returns the Current Color at a Point"""
        return self._colors[x][y]

    def getCurrent(self):
        """Returns the Current Color"""
        return self._current

    def setCurrent(self, color):
        """Set the Current Color"""
        self._current = color

    def drawLine(self, x0, y0, x1, y1, color):
        """Draws a Line"""
        hslope = abs(y1 - y0) > abs(x1 - x0)
        if hslope:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        if y0 < y1:
            ystep = 1
        else:
            ystep = -1
        dx = x1 - x0
        dy = abs(y1 - y0)
        error = 0
        y = y0
        for x in range(x0, x1 + 1):
            if hslope:
                self.fillColor(x, y, color)
            else:
                self.fillColor(y, x, color)
            error = error + dy
            if (error << 1) >= dx:
                y = y + ystep
                error = error - dx

    def drawTriangle(self, x0, y0, x1, y1, x2, y2, color):
        """"Draws and Fills a Triangle"""
        ymin = min(y0, y1, y2)
        ymax = max(y0, y1, y2)
        xmin = min(x0, x1, x2)
        xmax = max(x0, x1, x2)
        for y in range(ymin, ymax):
            for x in range(xmin, xmax):
                if ((y0 - y1)*x2 + (x1 - x0)*y2 + x0*y1 - x1*y0) != 0 and ((y0 - y2)*x1 + (x2 - x0)*y1 + x0*y2 - x2*y0) != 0:
                    gamma = float(((y0 - y1)*x + (x1 - x0)*y + x0*y1 - x1*y0))/float(((y0 - y1)*x2 + (x1 - x0)*y2 + x0*y1 - x1*y0))
                    beta = float(((y0 - y2)*x + (x2 - x0)*y + x0*y2 - x2*y0))/float(((y0 - y2)*x1 + (x2 - x0)*y1 + x0*y2 - x2*y0))
                    alpha = 1 - beta - gamma
                    if (0 <= alpha <= 1) and (0 <= beta <= 1) and (0 <= gamma <= 1):
                        self.fillColor(y, x, color)