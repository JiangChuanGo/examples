import threading
import time
# 导入 bottle 库
from bottle import  run, request, post
import json
import queue

import requests

import PySimpleGUI as sg

# Post 请求处理函数定义不用在 thread_work 里定义
@post('/msg')
def index():
    # 下一行代码不需要了，注释掉
    # print(request.body.read().decode("utf-8"))

    # 使用全局变量 que，也就是前面定义的队列
    global que

    # 解析客户端发来的 json 数据，转换为 Python dict
    # json.load 可以自动读取 ByteIO 对象，如果从 string 读取，要用 json.loads
    msg = json.load(request.body)

    # 打印调试信息，确保真的收到需要的数据了。
    print("msg from {}:{}".format(msg["from"], msg["msg"]))

    # 将 msg 对象放入队列，等会视窗线程会从队列另一端取出
    que.put(msg)
    return "<h1>OK</h1>"

# bottle 真正的死循环在 run 函数中，将它转移到 thread_work 里
# run(host='localhost', port=8080)


def thread_work(host, port):
    # 子线程里的死循环
    #while True:
    #    print("Web server runs on http://{}:{}".format(host, port))
    #    # 休眠 3s
    #    time.sleep(3)

    # run 函数本身就是死循环，上面的代码就不需要了
    run(host=host, port=port)

def send_msg(host, port, name, msg):
    # 按照约定，POST 数据是这样格式的字典，发送的时候会被转换为 Json 格式的字符串
    msg_obj = {"msg" : msg, "from" : name}

    # 使用 requests 库的 post 方法，向 http://host:port/msg 发送 msg_obj 转换成的 json 字符串，
    # 注意 post 函数的 data 参数就是是 msg_obj 经过 json 库转换后的结果。
    # 这里没有处理发送异常，如果希望完善一些，你应当在调用 send_msg 的时候捕获可能发生的异常。
    r = requests.post("http://{}:{}/msg".format(host, port) , data = json.dumps(msg_obj))


# 先询问用户一些有用的信息
hostInfoLayout = [
                [sg.Text("local port"), sg.Input("8080", size=(20, 1), justification="center", key = "-LPORT-")],
                [sg.Text("remote IP"), sg.Input("localhost", size=(20, 1), justification="center", key = "-HOST-")],
                [sg.Text("remote port"), sg.Input("8080", size=(20, 1), justification="center", key = "-PORT-")],
                [sg.Text("your name"), sg.Input(size=(20, 1), justification="center", key = "-NAME-")],
                [sg.Button("OK"), sg.Button("Cancel")]
]

popupWindow = sg.Window("Input your config", layout = hostInfoLayout)

event, values = popupWindow.read()

popupWindow.close()

del popupWindow

# 如果在询问阶段，用户就取消了，就退出程序
if event is None or event == "Cancel":
    exit()

# 这些信息在后面都有用
# remoteHost， 对方 IP
# remotePort， 对方 PORT
# userName， 本地用户名，发送者姓名
# localPort，本地 web 服务端口
remoteHost, remotePort, userName, localPort = values["-HOST-"], values["-PORT-"], values["-NAME-"], values["-LPORT-"]

# 硬编码的 HOST、PORT、SENDER 就不再需要了

# HOST 和 PORT 在编写 web 服务的时候，就已经定义过了
#HOST = "localhost"
#PORT = 8080

# 硬编码发送者姓名
#SENDER = "Jiangchuan"

# 创建队列，这一行在 worker.start() 之前
que = queue.Queue()

worker = threading.Thread(target=thread_work, args = ["0.0.0.0", localPort])
# 设置子线程为 Deamon 模式
worker.setDaemon(True)
worker.start()

# 继续增加一个 Input 输入消息，一个 Button 发送消息
# ###就显示一个多行文本框，大小是 50 * 5，单位是应为字符，并通过 disabled 禁止用户编辑内容，使其只读
layout = [  
    [sg.Multiline( size = (50, 5), key = "-MSG_SCREEN-", do_not_clear=True, disabled=True)],
    [sg.Input(key="-EDIT-", size = (50, 1))],
    [sg.Button("Send", key = "-SEND-")]
]

# 在程序标题上显示当前用户名
window = sg.Window("Msg APP:" + userName, layout = layout)

# 主线程里的死循环
while True:
    # 使用 read 函数异步模式，100 毫秒超时，通过 timeout_key 自定义了超时 event 的名称
    event, values = window.read(timeout = 100, timeout_key = "-TIMEOUT-")

    if event is None :
        break

    if event == "-TIMEOUT-":
        # 目前什么都不用做，不要在这里 print，会产生大量输出
        try:
            msg = que.get_nowait()
        except Exception:
            # 可能捕获 queue.Empty 异常，no new msg
            continue
        else:
            # que 中有新消息
            # 获取当前显示内容
            old_sreen = values["-MSG_SCREEN-"]

            # 获得消息正文、来源姓名
            new_msg = msg["msg"]
            from_ = msg["from"]

            # 按格式，拼接一行消息
            new_msg_line = "{}: {}".format(from_, new_msg) 

            # 将新消息追加到多行文本结尾
            new_screen = "{}{}".format(old_sreen, new_msg_line) if old_sreen != "" else new_msg_line

            # 将新数据更新到视窗
            window["-MSG_SCREEN-"].update(new_screen)
            continue

    if event == "-SEND-":
        old_sreen = values["-MSG_SCREEN-"]

        # 获得你输入的内容
        your_msg = values["-EDIT-"]

        # 发送消息
        send_msg(remoteHost, remotePort, userName, your_msg)

        # 将发送出去的消息，拼接为一条新的本地聊天记录，格式是 you: 消息
        new_msg_line = "{}: {}".format("you", your_msg) 

        # 将新记录追加到聊天记录尾部
        new_screen = "{}{}".format(old_sreen, new_msg_line) if old_sreen != "" else new_msg_line
        # 更新本地聊天记录框
        window["-MSG_SCREEN-"].update(new_screen)
        # 清空编辑框
        window["-EDIT-"].update("")
        continue


window.close()
