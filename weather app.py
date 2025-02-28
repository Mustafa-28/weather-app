from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import sys 
import requests
import os

class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.instructions = QLabel("Enter city name: ", self)
        self.City_Input = QLineEdit (self)
        self.Get_Weather_Button = QPushButton("Get Weather", self)
        self.Tempurature_Label = QLabel(self)
        self.Emoji_Label = QLabel(self)
        self.Weather_Label = QLabel(self)   
        self.UI()

    def UI(self):
        self.setWindowTitle("Weather")
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        self.setWindowIcon(QIcon(icon_path))
        Centeral_Widget = QWidget()
        Vbox = QVBoxLayout()
        Vbox.addWidget(self.instructions)
        Vbox.addWidget(self.City_Input)
        Vbox.addWidget(self.Get_Weather_Button)
        Vbox.addWidget(self.Tempurature_Label)
        Vbox.addWidget(self.Emoji_Label)
        Vbox.addWidget(self.Weather_Label)

        self.City_Input.setAlignment(Qt.AlignCenter)
        self.Tempurature_Label.setAlignment(Qt.AlignCenter)
        self.Emoji_Label.setAlignment(Qt.AlignCenter)
        self.Weather_Label.setAlignment(Qt.AlignCenter)
        Centeral_Widget.setLayout(Vbox)
        self.setCentralWidget(Centeral_Widget)

        self.instructions.setObjectName("instructions")
        self.City_Input.setObjectName("City_Input")
        self.Get_Weather_Button.setObjectName("Get_Weather_Button")
        self.Weather_Label.setObjectName("Weather_Label")
        self.Tempurature_Label.setObjectName("Tempurature_Label")
        self.Emoji_Label.setObjectName("Emoji_Label")

        self.setStyleSheet('''QLabel#instructions{
                           font-size: 50px;
                           border-radius: 10px;
                           padding: 7px;
                           margin: 7px;}

                           QLineEdit{
                           font-size: 60px;
                           background-color: hsl(188, 75%, 72%);
                           border-radius: 33px;
                           padding: 7px;
                           margin: 7px;}

                           QPushButton{
                           font-size: 40px;
                           background-color: hsl(188, 4%, 56%);
                           border-radius: 11px;
                           padding: 7px;
                           margin: 7px;}

                           QPushButton#Get_Weather_Button:hover{
                           background-color: hsl(188, 4%, 76%);}
                           QLabel#Weather_Label{
                           font-size: 50px;}

                           QLabel#Tempurature_Label{
                           font-size: 80px;
                           padding: 7px;
                           margin: 7px;}

                           QLabel#Emoji_Label{
                           font-family: Segoe UI Emoji;
                           font-size: 155px;
                           padding: 5px;
                           margin: 5px;}''') 
        self.City_Input.setPlaceholderText("Enter city name: ")
        self.Get_Weather_Button.clicked.connect(self.Get_Weather)
        self.City_Input.returnPressed.connect(self.Get_Weather)
        
    def Get_Weather(self):
        api_key = "067f1b6331c9c149ac7c3b7c9894816f"
        try:
            city = self.City_Input.text()
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if response.status_code ==200:
                self.Display_Weather(data)
        except requests.exceptions.HTTPError as Http_error:
            match response.status_code:
                case 400:
                    self.Display_Error("Bad Request\nPlease check your input")
                case 401:
                    self.Display_Error("Unauthorized \nInvalid API")
                case 403:
                    self.Display_Error("Forbidden \nAccess is denied")
                case 404:
                    self.Display_Error("Not found\nCity not found")
                case 500:
                    self.Display_Error("Internal Server Error \nPlease try again later")
                case 502:
                    self.Display_Error("Bad Gateway\nPlease try again later")
                case 503:
                    self.Display_Error("Service Unavailable\nPlease try again later")
                case 504:
                    self.Display_Error("Gateway Timeout\nPlease check your internet connection or try again later")
                case _:
                    self.Display_Error(f"HTTP Error {Http_error}")

        except requests.exceptions.ConnectionError:
            self.Display_Error("Connection Error\nPlease check your internet connection")
        except requests.exceptions.Timeout:
            self.Display_Error("Timeout \nPlease try again later")
        except requests.exceptions.TooManyRedirects:
            self.Display_Error("Too Many Redirects Error\nPlease check the url")
        except requests.exceptions.RequestException as Req_error:
            self.Display_Error(f"Request Error\n{Req_error}")

    def Display_Weather(self, data):
        temp_K = int(data['main']['temp'])
        temp_C = str(temp_K - 273)+"°"
        self.Tempurature_Label.setStyleSheet("font-size:80px;")
        self.Tempurature_Label.setText(temp_C)
        weather = data['weather'][0]['description']
        self.Weather_Label.setText(weather)
        The_id = data['weather'][0]['id']
        if 200 <= The_id <= 232:
            self.Emoji_Label.setText("⛈️")
        elif 300 <= The_id <= 321:
            self.Emoji_Label.setText("🌦️")
        elif 500 <= The_id <= 531:
            self.Emoji_Label.setText("🌧️")
        elif 600 <= The_id <= 622:
            self.Emoji_Label.setText("❄️")
        elif 701 <= The_id <= 761:
            self.Emoji_Label.setText("🌫️")
        elif 762 == The_id :
            self.Emoji_Label.setText("🌋")
        elif 771 == The_id <= 781:
            self.Emoji_Label.setText("🌪️")
        elif 800 == The_id :
            self.Emoji_Label.setText("☀️")
        elif 801 <= The_id <= 804:
            self.Emoji_Label.setText("☁️")    

    def Display_Error(self, message):
        self.Tempurature_Label.setStyleSheet("font-size: 30px;")
        self.Tempurature_Label.setText(message)

def main():
    app = QApplication(sys.argv)
    Weather_app = Main_Window()
    Weather_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()