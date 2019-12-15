# encoding = utf-8

import PySimpleGUI as sg

# 只定义一个简单的Tex 显示计数，一个按钮接受用户触发

layout = [
    [sg.Text("0", justification= "center", key = "-TEXT-")],
    [sg.OK()]
]


window = sg.Window("APP", layout = layout)

# 计数变量
count = 0

while True:

    # 设置超市时间，就切换到异步模式，注意超时时间单位是毫秒
    event, values = window.read(timeout = 1 * 1000)
    # 处理点击 X 退出的情况
    if event is None:
        break

    # 处理超时
    if event == "__TIMEOUT__":
        count += 1
        # 更新视窗计数
        window["-TEXT-"].update(str(count))
        continue

    # 未指定 key 的按钮组件，事件是按钮上的 字符
    if event == "OK":
        print("用户点击我了！")
        continue

# 记得关闭 window，保证在所有平台都能正常释放资源
window.close()