import PySimpleGUI as sg
import requests
import json

from china_regions import regions


def get_weather(city):
    # 在线环境不支持中文输入，所以我改用城市编号的接口，如果你在电脑上开发，就不受影响
    # 注释掉旧接口，不再使用城市编码查询天气
    # r = requests.get("http://wthrcdn.etouch.cn/weather_mini?citykey=" + city)
    try:
        r = requests.get("http://wthrcdn.etouch.cn/weather_mini?city=" + city)
        result = json.loads(r.text)
        weather = result["data"]["forecast"][0]["type"]
    except:
        sg.Popup("Some error occured!")
        exit()

    return weather

def update_city_weather(window, output_id, city):
    weather = get_weather(city)

    print(f"The weather of {city} is: {weather}")

    # 找到天气输入框
    weather_wind = window[output_id]

    # 将天气更新到输入框
    weather_wind.update(weather)

# 让所有文本居中
sg.SetOptions(text_justification='center') 

# 初始化省列表
province_city = regions.province_city

provinces = list(province_city.keys())


# 蓝图不需要放到循环中, 注意市区的默认选项处理
layout = [ 
           [ 
                sg.Text("省", size = (20, 1)), sg.Combo(provinces, size=(10, 1), default_value=provinces[0], change_submits=True, key = "-PROVINCE-"),
                sg.Text("市", size = (20, 1)), sg.Combo(province_city[provinces[0]], default_value=province_city[provinces[0]][0], size=(10, 1), change_submits=True, key = "-CITY-")
           ],
           [ sg.Text("Weather", size = (20, 1)), sg.Input(key = "-WEATHER-") ] #,
         ]

# 视窗也只需要创建一次，不要放到循环里
# 添加 finalize ，以便在 read 之前操作 UI 资源
window = sg.Window("Weather App", layout, finalize=True)

# 更新初始城市天气，也就是北京市的天气
update_city_weather(window, "-WEATHER-", province_city[provinces[0]][0])

while True:
    event, values = window.read()

    print(event, values)

    # 当点击 window 右上角的 X，event 是 None，此时应当退出循环
    if event in (sg.WIN_CLOSED, "Quit", "Cancel"):
        break


    # 更新市列表
    if event == "-PROVINCE-":

        # 获取当前省份
        province = values["-PROVINCE-"]

        # 查询当前省份的所有市
        citys = province_city[province]

        # 更新市列表，不要忘记更新默认值
        window["-CITY-"].Update(values = citys, set_to_index=0, value=citys[0])
    
        # 为默认选项，更新天气
        city = citys[0]

        # 更新显示天气
        update_city_weather(window, "-WEATHER-", city)

    if event == "-CITY-":
        
        # values 是一个字典，访问可输入组件的 key（定义蓝图时指定了这个参数）可以获得组件的输入
        city = values["-CITY-"]
        
        # 市区为空, 不处理
        if values["-CITY-"] == "":
            continue

        # 更新显示天气
        update_city_weather(window, "-WEATHER-", city)

# 当退出循环的时候，就是程序退出之时，关掉 window
window.close()
