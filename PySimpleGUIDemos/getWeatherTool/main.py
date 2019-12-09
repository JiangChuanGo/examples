import PySimpleGUI as sg
import requests
import json

def get_weather(city):
    # 在线环境不支持中文输入，所以我改用城市编号的接口，如果你在电脑上开发，就不受影响
    # 注释掉旧接口，不再使用城市编码查询天气
    # r = requests.get("http://wthrcdn.etouch.cn/weather_mini?citykey=" + city)
    r = requests.get("http://wthrcdn.etouch.cn/weather_mini?city=" + city)
    result = json.loads(r.text)
    return result["data"]["forecast"][0]["type"]


# 让所有文本居中
sg.SetOptions(text_justification='center') 

# 蓝图不需要放到循环中
layout = [ 
           #[ sg.Text("City", size = (20, 1)), sg.Input(key = "-CITY-") ],
           [ sg.Text("City", size = (20, 1)), sg.Combo(("北京", "上海", "深圳"), size=(10, 1), default_value="上海", change_submits=True, key = "-CITY-")],
           [ sg.Text("Weather", size = (20, 1)), sg.Input(key = "-WEATHER-") ] #,
           #[ sg.Button("Submit")]
         ]

# 视窗也只需要创建一次，不要放到循环里
window = sg.Window("Weather App", layout)

while True:
  event, values = window.read()

  print(event, values)

  # 当点击 window 右上角的 X，event 是 None，此时应当退出循环
  if event is None:
    break

  # values 是一个字典，访问可输入组件的 key（定义蓝图时指定了这个参数）可以获得组件的输入
  city = values["-CITY-"]

  weather = get_weather(city)

  print(weather)

  # 找到天气输入框
  weather_wind = window["-WEATHER-"]

  # 将天气更新到输入框
  weather_wind.update(weather)

  # 程序已经不会直接退出了，下一行就不需要了
  # window.read()

# 当退出循环的时候，就是程序退出之时，关掉 window
window.close()
