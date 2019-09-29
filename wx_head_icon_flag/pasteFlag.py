from PIL import Image
import numpy as np
from io import BytesIO
import requests

# 图片切割为正方形
def crop_square(img):
    x, y = img.size
    center = (int(x/2), int(y/2))
    length = int(min(x, y)/2)
    left_top = (center[0] - length, center[1] - length)
    right_buttom = (center[0] + length, center[1] + length)
    
    new_img = img.crop(left_top + right_buttom)
    return new_img


# 加载 互联网 上维护的图像
def img_from_url(img_url):
	
	res = requests.get(img_url, stream=True)

	if res.status_code != 200:
    		print("cannot get flag img: {}".format(flag_img_url))
    		exit()
    
	byte_stream = BytesIO(res.content)
	return Image.open(byte_stream)


# 为 head：Image 增加国旗
def _add_flag(head):
	THRESHOLD = 100 
	FLAG_IMG_URL = "https://raw.githubusercontent.com/JiangChuanGo/examples/master/wx_head_icon_flag/flag.jpg"

	head = head.convert("RGBA")
	head = crop_square(head)

	global localFlag

	if localFlag:
		print("use local Flag")
		flag = Image.open(localFlag).convert("RGBA")
	else:
		flag = img_from_url(FLAG_IMG_URL)

	grayFlag = flag.convert("L")
	grayFlag = np.array(grayFlag)

	mask = (grayFlag > THRESHOLD).astype(np.uint8) * 255

	resizedHead = head.resize(flag.size, Image.ANTIALIAS)

	headLayer = resizedHead.copy()

	maskLayer = Image.fromarray(np.uint8(mask))

	headLayer.paste(flag, (0, 0), mask= maskLayer)
	
	return headLayer.convert("RGB")

localFlag = False

def set_local_flag(filename = None):
	global localFlag 
	localFlag = filename
	

# 指定文件名 url 或者 Image 对象均可
def add_flag(filename=None, url=None, img = None):
	if filename:
		img = Image.open(filename)
	elif url:
		img = img_from_url(url)
	return _add_flag(img)

if __name__ == "__main__":
    add_flag("head.jpeg").show()
