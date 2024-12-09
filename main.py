from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QWidget, QPushButton,QVBoxLayout
from PyQt5.QtCore import Qt
import sys
import requests
from dotenv import load_dotenv
import os
from PyQt5.QtGui import QPixmap
from io import BytesIO

load_dotenv()

class WeatherApp(QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Weather App")
    self.setGeometry(700,300,400,500)
    self.city_label=QLabel("Enter City Name",self)
    self.city_input=QLineEdit(self)
    self.get_temperature=QPushButton("Get Weather Updates",self)
    self.temperature_label=QLabel(self)
    self.emoji_label=QLabel(self)
    self.description_label=QLabel(self)
    self.initUI()

  def initUI(self):
    vbox=QVBoxLayout()
    vbox.addWidget(self.city_label)
    vbox.addWidget(self.city_input)
    vbox.addWidget(self.get_temperature)
    vbox.addWidget(self.temperature_label)
    vbox.addWidget(self.emoji_label)
    vbox.addWidget(self.description_label)

    self.setLayout(vbox)
    self.city_label.setAlignment(Qt.AlignCenter)
    self.city_input.setAlignment(Qt.AlignCenter)
    self.temperature_label.setAlignment(Qt.AlignCenter)
    self.emoji_label.setAlignment(Qt.AlignCenter)
    self.description_label.setAlignment(Qt.AlignCenter)

    
    self.city_label.setObjectName("city_label")
    self.city_input.setObjectName("city_input")
    self.temperature_label.setObjectName("temperature_label")
    self.emoji_label.setObjectName("emoji_label")
    self.get_temperature.setObjectName("get_temperature")
    self.description_label.setObjectName("description_label")

    self.setStyleSheet("""
                        QLabel,QPushButton{
                        font-family:calibiri;
                        }
                        QLabel#city_label{
                        font-style:italic;
                        font-size:40px;
                        }
                        QLineEdit#city_input{
                        font:30px;
                        }
                        QPushButton#get_temperature{
                        font-size:30px;
                        font-weight:bold;
                        background-color:grey;
                        }
                        QLabel#temperature_label{
                        font-size:30px;
                        }
                        QLabel#emoji_label{
                        font-size:60px;
                        font-family:segoe UI emoji;
                        }
                        QLabel#description_label{
                        font-size:30px;
                        }

    """)

    self.get_temperature.clicked.connect(self.get_weather)

  def get_weather(self):
    api_key=os.getenv("WEATHER_API_KEY")
    url=os.getenv("WEATHER_API_URL")
    city=self.city_input.text()
    try:
      response=requests.get(f"{url}{city}&appid={api_key}")
      response.raise_for_status()
      data=response.json()
      self.display_weather(data)

    except requests.exceptions.HTTPError:
      match response.status_code:
        case 400:
          self.error_message(f"Bad request\n please check your input")
        case 401:
          self.error_message(f"Unauthorised access\n Please check api key")
        case 403:
          self.error_message(f"Access Forbiden")
        case 404:
          self.error_message(f"Not Found\n Please check City name")
        case 500:
          self.error_message(f"Internal server error")

    except requests.exceptions.RequestException as e:
      self.error_message(e)

  def error_message(self,message):
    self.temperature_label.setText(message)
    self.description_label.clear()
    self.emoji_label.clear()


  def display_weather(self,data):
    temp=data['main']['temp']-273
    weather_description=data['weather'][0]['description']
    icon_code=data['weather'][0]['icon']
    self.temperature_label.setText(f"{temp:.0f}")
    self.description_label.setText(weather_description)
    try:
      response=requests.get(f"https://openweathermap.org/img/wn/{icon_code}@2x.png")
      response.raise_for_status()
      image_data=BytesIO(response.content)
      pixmap=QPixmap()
      pixmap.loadFromData(image_data.getvalue())
      self.emoji_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))

    except requests.exceptions.RequestException as e:
      self.emoji_label.setText('Failed to load image')


def main():
  app=QApplication([])
  wapp=WeatherApp()
  wapp.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()