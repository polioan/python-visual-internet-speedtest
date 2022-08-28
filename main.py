from datetime import datetime
from entryPoint import App
from graph import Graph
from speedtestWrapper import SpeedtestWrapper

def drawTextTable(table, left = 0, top = 0, dist = 20, color = (0, 0, 0)):
	for i in range(len(table)): app.screen.blit(app.font.render(table[i], True, color), (left, top + i * dist))

if __name__ == '__main__':
  app = App()

  graphDownload = Graph(app.screen, app.font)
  graphUpload = Graph(app.screen, app.font); graphUpload.pointColor = (20, 15, 183); graphUpload.lineColor = (20, 15, 230); graphUpload.left = 520

  SpeedtestWrapper("singleThread", lambda: app.running, lambda v: graphDownload.append(v), lambda v: graphUpload.append(v))
  startTime = datetime.today()

  @app.mainLoop
  def main():
    graphDownload.draw()
    graphUpload.draw()

    drawTextTable([
		"Download speed",
		"Кол-во тестов: " + str(len(graphDownload)),
		"Средняя скорость: " + "{:.2f}".format(graphDownload.getAverage()),
    "Общее время работы: " + str(datetime.today() - startTime)
		], 10, 520)

    drawTextTable([
		"Upload speed",
		"Кол-во тестов: " + str(len(graphUpload)),
		"Средняя скорость: " + "{:.2f}".format(graphUpload.getAverage())
		], 520, 520)

  __import__('os')._exit(0)