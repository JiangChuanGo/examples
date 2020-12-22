def get_weather_img(weather):
    weather_dict = {
        "雨" : "rainy.png",
        "阴" : "cloudy.png",
        "云" : "cloudy.png",
        "晴" : "sunny.png",
        "风" : "windy.png",
        "雪" : "snowy.png"
    }

    default = "晴"
    filename = "sunny.png"

    cn_weathers = list(weather_dict.keys())
    for cn_weather in cn_weathers:
        if cn_weather in weather:
            filename = weather_dict[cn_weather]
            break
    else:
        filename = weather_dict[default]

    return "./weather_img/imgs/" + filename
