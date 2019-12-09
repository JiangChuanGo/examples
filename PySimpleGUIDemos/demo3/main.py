import PySimpleGUI as sg
import requests
import json

def get_weather(city):
    # 在线环境不支持中文输入，所以我改用城市编号的接口，如果你在电脑上开发，就不受影响
    r = requests.get("http://wthrcdn.etouch.cn/weather_mini?citykey=" + city)
    result = json.loads(r.text)
    return result["data"]["forecast"][0]["type"]


# 让所有文本居中
sg.SetOptions(text_justification='center') 

layout = [ 
           [ sg.Text("City", size = (20, 1)), sg.Input(key = "-CITY-") ],
           [ sg.Text("Weather", size = (20, 1)), sg.Input(key = "-WEATHER-") ],
           [ sg.Button("Submit")]
         ]

window = sg.Window("Weather App", layout)

event, values = window.read()

print(event, values)

# values 是一个字典，访问可输入组件的 key（定义蓝图时指定了这个参数）可以获得组件的输入
city = values["-CITY-"]

weather = get_weather(city)

print(weather)

# 找到天气输入框
weather_wind = window["-WEATHER-"]

# 将天气更新到输入框
weather_wind.update(weather)

# 如果没有这一行，程序会一闪而退，你根本看不到效果
window.read()

window.close()
