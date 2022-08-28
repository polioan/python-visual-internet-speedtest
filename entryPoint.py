import pygame as pg

class Config:
  width = 1030
  height = 600
  appName = 'Speedtest'
  fps = 60
  backgroundColor = (255, 255, 255)
  fontSize = 20

class App:
  def __init__(self):
    pg.init()
    pg.mixer.init()
    pg.font.init()

    pg.display.set_caption(Config.appName)

    self.screen = pg.display.set_mode((Config.width, Config.height))
    self.clock = pg.time.Clock()
    self.running = True
    self.onEventFunction = None
    self.font = pg.font.SysFont("Calibri", Config.fontSize)

  def onEvent(self, func):
    self.onEventFunction = func

  def mainLoop(self, func):
    while self.running:
      self.clock.tick(Config.fps)
      for event in pg.event.get():
        if event.type == pg.QUIT:
          self.running = False
        else:
          self.onEventFunction and self.onEventFunction(event)
      self.screen.fill(Config.backgroundColor)
      func()
      pg.display.flip()

    pg.quit()