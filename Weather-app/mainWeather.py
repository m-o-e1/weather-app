# sys - meeans systems as it hanfles sys variables for python interpreter

import sys
import os
import requests
from dotenv import load_dotenv

from PyQt5.QtWidgets import (
QApplication, QWidget,
QLabel, QLineEdit, 
QPushButton, QVBoxLayout) #widgets 

from PyQt5.QtCore import Qt

load_dotenv()
##

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.resize(400, 300)
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel("Sunny", self)
        self.initUI()


    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
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
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")


        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;          
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;            
            }
            QLineEdit#city_input{
                font_size: 40px;         
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            Qlabel#description_label{
                font-size: 50px;
            }
        """)
        self.get_weather_button.clicked.connect(self.get_weather)

    
    def get_weather(self):
        
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            self.display_error("API key is missing")
            return
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
             self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    print("Bad request \n Please check your input")

                case 401:
                    print("Unauthorized \n Invalid API key")

                case 4003:
                    print("Forbidden \n Acces Denied")

                case 4004:
                    print("Not Found \n City Not Found")

                case 500:
                    print("Internal Server Error \n Please try again later")
               
                case 502:
                    print("Bad Gateway \n Invalid Response From Server")

                case 503:
                    print("Service Unavailable \n Server is Down")

                case 504:
                    print("Gateway Timeout \n No Response from Server")

                case _:
                    print(f"HTTP error occured\n {http_error}")

        except requests.exceptions.ConnectionError:
            print("Connection Error:\nCheck your internet connection")

        except requests.exceptions.Timeout:
            print("Timeout Error:\nThe request timed out")

        except requests.exceptions.TooManyRedirects:
            print("Too many redirects:\nCheck the URL")

        except requests.exceptions.RequestException as req_error:
            print(f"Request Error:\n{req_error}")

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
    
    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature_k = data["main"]['temp']
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9/5) - 459.67
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

       
        self.temperature_label.setText(f"{temperature_f:.0f} ℉")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)



    @staticmethod
    def get_weather_emoji(weather_id):
      if 200 <= weather_id <= 232:
          return "🌩️"
      elif 300 <= weather_id <= 321:
          return "🌦️"
      elif 500 <= weather_id <= 531:
          return "🌧️"
      elif 600 <= weather_id <= 622:
          return "❄️"
      elif 701 <= weather_id <= 741:
          return "🌁"
      elif weather_id == 762:
          return "🌋"
      elif weather_id == 771:
          return "💨"
      elif weather_id == 781:
          return "🌪️"
      elif weather_id == 800:
          return "☀️"
      elif 801 <= weather_id <= 804:
          return "☁️"
      else:
          return "ERROR"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.setWindowTitle("Weather App")
    weather_app.resize(400, 300)
    weather_app.show()

    sys.exit(app.exec_())
