import PySimpleGUI as sg
import rsa
import base64

# 一些配置
CONF = {
    'key_len' : 2048,
    'MSG_HEAD': r"*\/*",
    'MSG_HEAD_LEN' : len(r"*\/*")
}

# 保存全局数据
GLOBAL_CTX = {
    'pub' : None,
    'pub_pk' : None,
    'priv' : None,
    'priv_pk' : None,

    'remote_pub' : None,
    'remote_pub_pk' : None
}

# 用一个 OK 弹窗提示消息，如果要改用其他实现，修改 alert 的实现即可。
alert = sg.popup_ok


# 布局
layout = [
        [sg.Multiline("", key='-TEXT-PAD-',  size=(50,20), enable_events=True)],
        [sg.Button("加 密", key="-ACT-"), sg.Button("退出", key="QUIT")]
    ]

# 创建密钥对，原始数值形式 + pem 格式
def create_keys():
    pub, priv = rsa.newkeys(CONF['key_len'])
    pub_pk = pub.save_pkcs1().decode('utf8')
    priv_pk = priv.save_pkcs1().decode('utf8')

    return pub, priv, pub_pk, priv_pk


# 显示一个弹窗，包含一个标题和多行文本输入
def show_titled_popup(title, msg):
    layout = [
        [sg.Text(title)],
        [sg.Multiline(msg,size=(50,20))],
        [sg.Button("OK"), sg.Button("Cancel")]

    ]

    window = sg.Window("提示", layout, finalize=True)
    out = window.read()
    window.close()

    return out



# 创建本地密钥对，并保存在全局字典中
def create_local_keys():
   
    pub, priv, pub_pk, priv_pk = create_keys()

    GLOBAL_CTX["pub"] = pub
    GLOBAL_CTX["priv"] = priv
    GLOBAL_CTX["pub_pk"] = pub_pk
    GLOBAL_CTX["priv_pk"] = priv_pk


# 更新对方公钥记录，用于处理对方发来的公钥信息
def update_remote_pub(pub_pk):
    GLOBAL_CTX["remote_pub_pk"] = pub_pk
    GLOBAL_CTX["remote_pub"] = rsa.PublicKey.load_pkcs1(pub_pk)


# 解密消息
def decrypt_msg(msg):
    # 先将消息从 base64 编码还原为二进制数据
    raw_msg = base64.b64decode(msg)

    # 解密
    plain_msg = rsa.decrypt(raw_msg, GLOBAL_CTX["priv"]).decode("utf-8")

    return plain_msg


# 加密消息
def encrypt_msg(msg):
    encrypted = rsa.encrypt(msg.encode("utf8"), GLOBAL_CTX["remote_pub"])
    encrypted_str = base64.b64encode(encrypted).decode("utf-8")

    return encrypted_str




###### MAIN STARTS HERE #########


alert("提示！", "即将为本次通信创建密钥，这大概需要 10 秒，请等待！")

create_local_keys()

ev, val = show_titled_popup("请将下面的公钥发给对方", GLOBAL_CTX["pub_pk"])

if "OK" != ev:
    exit()

ev, val = show_titled_popup("请填写对方的公钥：", "")
if "OK" != ev:
    exit()

update_remote_pub(val[0])



# 添加 finalize ，以便在 read 之前操作 UI 资源
window = sg.Window("RSA-crypto", layout, finalize=True)


while True:
    event, values = window.read()

    print(event, values)

    # 当点击 window 右上角的 X，event 是 None，此时应当退出循环
    if event in (sg.WIN_CLOSED, "Quit", "QUIT", "Cancel"):
        break

    if event == "-TEXT-PAD-":
        if values['-TEXT-PAD-'].startswith(CONF['MSG_HEAD']):
            window['-ACT-'].update("解 密")
        else:
            window['-ACT-'].update("加 密")

    if event == "-ACT-":
        if window['-ACT-'].GetText() == "解 密":
            if not values['-TEXT-PAD-'].startswith(CONF['MSG_HEAD']):
                alert("错误！", "错误的密文.")
                continue
            text = values['-TEXT-PAD-']
            text = text[CONF['MSG_HEAD_LEN']:]
            try:
                msg = decrypt_msg(text)
            except:
                alert("错误!", "无法解密，密钥可能不匹配，如果确定密文没问题，那么你和对方都需要关闭程序，重新创建密钥。")
                continue

            window['-TEXT-PAD-'].update(msg)
        elif window['-ACT-'].GetText() == "加 密":
            if values['-TEXT-PAD-'].startswith(CONF['MSG_HEAD']):
                alert("错误！", f"请不要以 {CONF['MSG_HEAD']} 开头.")
                continue

            msg = values['-TEXT-PAD-']
            text = encrypt_msg(msg)
            text = CONF['MSG_HEAD'] + text
            window['-TEXT-PAD-'].update(text)


window.close()

