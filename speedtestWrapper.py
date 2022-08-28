from speedtest import Speedtest
from threading import Thread
from time import sleep

class SpeedtestWrapper:
  MB = 1024 * 1024

  def stDownload(self):
    return self.st.download() / self.MB
		
  def stUpload(self):
    return self.st.upload() / self.MB
	
  def speedtestDownloadFunc(self):
    try: self.onDownloadUpd and self.onDownloadUpd(self.stDownload())
    except: pass
			
  def speedtestUploadFunc(self):
    try: self.onUploadUpd and self.onUploadUpd(self.stUpload())
    except: pass

  def speedtestDownloadThread(self):
    while self.whenEndFunc():
      self.speedtestDownloadFunc()
      sleep(self.sleepTime)
			
  def speedtestUploadThread(self):
    while self.whenEndFunc():
      self.speedtestUploadFunc()
      sleep(self.sleepTime)
			
  def speedtestSingleThread(self):
    while self.whenEndFunc():
      self.speedtestDownloadFunc()
      self.speedtestUploadFunc()
      sleep(self.sleepTime)

  def onDownload(self, func):
    self.onDownloadUpd = func

  def onUpload(self, func):
    self.onUploadUpd = func

  def __init__(self, mode = "singleThread", whenEndFunc = lambda: True, onDownloadUpd = None, onUploadUpd = None):
    self.sleepTime = 0
    self.st = Speedtest()
    self.whenEndFunc = whenEndFunc
    self.onDownloadUpd = onDownloadUpd
    self.onUploadUpd = onUploadUpd
		
    if mode == "singleThread":
      Thread(target=self.speedtestSingleThread).start()
    elif mode == "doubleThread":
      Thread(target=self.speedtestDownloadThread).start()
      Thread(target=self.speedtestUploadThread).start()