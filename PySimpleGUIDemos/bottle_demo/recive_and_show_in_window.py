import threading
import time
# 导入 bottle 库
from bottle import  run, request, post
import json
import queue

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

HOST = "localhost"
PORT = 8080

# 创建队列，这一行在 worker.start() 之前
que = queue.Queue()

worker = threading.Thread(target=thread_work, args = [HOST, PORT])
# 设置子线程为 Deamon 模式
worker.setDaemon(True)
worker.start()

# 就显示一个多行文本框，大小是 50 * 5，单位是应为字符，并通过 disabled 禁止用户编辑内容，使其只读
layout = [  [sg.Multiline( size = (50, 5), key = "-MSG_SCREEN-", do_not_clear=True, disabled=True)]]

window = sg.Window("Msg App", layout = layout)

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


window.close()
