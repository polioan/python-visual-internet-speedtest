import pygame as pg
from math import isinf

def div(a, b):
  try:
    return a / b
  except ZeroDivisionError:
    return 0

def map(value, low1, high1, low2, high2):
  return low2 + (high2 - low2) * div(value - low1, high1 - low1)

class Graph:
  def __init__(self, screen, font, pointsToAppend = []):
    self.screen = screen
    self.font = font

    self.rectColor = (203, 212, 228)
    self.internalRectColor = (117, 140, 183)
    self.pointColor = (183, 15, 23)
    self.lineColor = (230, 15, 23)
    self.textColor = (0, 0, 0)
    self.pointSize = 2

    self.__internalRectOffset = 15

    self.__left = 10
    self.__top = 10
    self.__width = 500
    self.__height = 500

    self.__points = []

    self.__lowerLimit = float('inf')
    self.__upperLimit = float('-inf')

    self.__drawCachedPoints = []
    self.areLimitUpdate = True

    if len(pointsToAppend) > 0: self.append(pointsToAppend)

  @property
  def internalRectOffset(self): return self.__internalRectOffset
  @property
  def left(self): return self.__left
  @property
  def top(self): return self.__top
  @property
  def width(self): return self.__width
  @property
  def height(self): return self.__height
  @property
  def lowerLimit(self): return self.__lowerLimit
  @property
  def upperLimit(self): return self.__upperLimit
  @property
  def points(self): return self.__points

  @internalRectOffset.setter
  def internalRectOffset(self, value): self.__internalRectOffset = value; self.__onReCacheDrawPoints()
  @left.setter
  def left(self, value): self.__left = value; self.__onReCacheDrawPoints()
  @top.setter
  def top(self, value): self.__top = value; self.__onReCacheDrawPoints()
  @width.setter
  def width(self, value): self.__width = value; self.__onReCacheDrawPoints()
  @height.setter
  def height(self, value): self.__height = value; self.__onReCacheDrawPoints()
  @lowerLimit.setter
  def lowerLimit(self, value): self.__lowerLimit = value; self.__onReCacheDrawPoints()
  @upperLimit.setter
  def upperLimit(self, value): self.__upperLimit = value; self.__onReCacheDrawPoints()
  @points.setter
  def points(self, value): self.__points = value; self.__onReCacheDrawPoints()

  def __len__(self): return len(self.__points)

  def restoreLimits(self):
    self.__lowerLimit = min(self.__points)
    self.__upperLimit = max(self.__points)
    self.__onReCacheDrawPoints()

  def updateLimits(self, value, reCache = True):
    if self.areLimitUpdate:
      areUpdate = False
      if value < self.lowerLimit:
        self.__lowerLimit = value
        areUpdate = True
      if value > self.upperLimit:
        self.__upperLimit = value
        areUpdate = True
      if areUpdate and reCache: self.__onReCacheDrawPoints()

  def __onReCacheDrawPoints(self):
    self.__drawCachedPoints.clear()
    length = len(self)
    for i in range(length):
      x = map(i, 0, length - 1, self.left + self.internalRectOffset, self.left + self.width - self.internalRectOffset)
      y = map(self.points[i], self.lowerLimit, self.upperLimit, self.top - self.internalRectOffset + self.height, self.top + self.internalRectOffset)
      self.__drawCachedPoints.append((int(x), int(y)))

  def __onAppend(self, value):
    self.updateLimits(value, False)
    self.__points.append(value)

  def append(self, *values):
    for value in values:
      if (type(value) is list) or (type(value) is tuple):
        for listValue in value:
          self.__onAppend(listValue)
      else:
        self.__onAppend(value)
    self.__onReCacheDrawPoints()

  def drawRect(self):
    pg.draw.rect(self.screen, self.rectColor, (self.left, self.top, self.width, self.height) )

  def drawInternalRect(self):
    doubleOffset = self.internalRectOffset * 2
    pg.draw.rect(self.screen, self.internalRectColor, (self.left + self.internalRectOffset, self.top + self.internalRectOffset, self.width - doubleOffset, self.height - doubleOffset) )

  def textFormat(self, value, isUpper):
    num = ''
    if not isinf(value):
      num = '{:.2f}'.format(value)
    return ('Max ' if isUpper else 'Min ') + num

  def drawText(self):
    self.screen.blit(self.font.render(self.textFormat(self.upperLimit, True), True, self.textColor), (self.left, self.top))
    self.screen.blit(self.font.render(self.textFormat(self.lowerLimit, False) , True, self.textColor), (self.left, self.top + self.height - self.font.get_height()))

  def drawPoints(self):
    for point in self.__drawCachedPoints:
      pg.draw.circle(self.screen, self.pointColor, point, self.pointSize)

  def drawLines(self):
    for i in range(len(self.__drawCachedPoints) - 1):
      try:
        pg.draw.aaline(self.screen, self.lineColor, self.__drawCachedPoints[i], self.__drawCachedPoints[i + 1])
      except IndexError: return

  def draw(self):
    self.drawRect()
    self.drawLines()
    self.drawPoints()
    self.drawText()

  def drawTransparent(self):
    self.drawLines()
    self.drawPoints()

  def getMid(self):
    return (self.lowerLimit + self.upperLimit) / 2

  def getAverage(self):
    return sum(self.__points, 0.0) / max(len(self), 1)