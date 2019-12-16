import threading
import time

def thread_work(host, port):
    # 子线程里的死循环
    while True:
        print("Web server runs on http://{}:{}".format(host, port))
        # 休眠 3s
        time.sleep(3)

HOST = "localhost"
PORT = 8080

worker = threading.Thread(target=thread_work, args = [HOST, PORT])
worker.start()

# 主线程里的死循环
while True:
    print("Main thread running~")
    # 休眠 2s
    time.sleep(1)
