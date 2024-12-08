from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QWidget, QPushButton,QHBoxLayout
from PyQt5.QtCore import Qt
import sys
import requests

class WeatherApp(QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Weather App")
    self.setGeometry(700,300,400,500)
    self.initUI()

  def initUI(self):
    pass


def main():
  app=QApplication([])
  wapp=WeatherApp()
  wapp.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()