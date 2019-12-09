import PySimpleGUI as sg
layout = [ [sg.Text("Name"), sg.Input(key="-NAME-")], [sg.Button("OK", key="-OK-")] ]

# 阻塞，直到用户点击按钮才返回
window = sg.Window("Hello App", layout)

# window.read() 返回的是 tuple，这里直接将 tuple 解包为 event 和 values 备用
event, values = window.read()

# 拼接字符串, 我刚发现这款 online IDE 不支持中文
info = "Welcome " + values["-NAME-"]

# 弹窗，演示多行信息
sg.Popup(info, "one more line", "another line")

# 最后，关闭 windows 是个好习惯
window.close()
