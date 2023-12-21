# encoding:utf-8
from pygamescript import GameScript, ImageTemplate
from minidevice import DroidCast, Minitouch
from adbutils import adb
from src.config import IMAGES_DIR
from time import sleep
from src.tasks.base.ready.task import ready
from src.tasks.base.settle.task import settleFail, settleWin
import requests
import time
import json

# my_token = ""


def pushPlus(token, title, content):
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": token,
        "title": title,
        "content": content
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=body, headers=headers)


device = adb.device_list()[0].serial

ld = GameScript(device, capMethod=DroidCast, touchMethod=Minitouch)

while 1:
    ready(ld, isExit=False)
    settleWin(ld)
    settleFail(ld)
    if ld.findAndClick(ImageTemplate(IMAGES_DIR + "超鬼王/探索鬼王.png", region=[1000, 500, 1280, 720])):
        sleep(3)
        if ld.find(ImageTemplate(IMAGES_DIR + "超鬼王/探索鬼王.png", region=[1000, 500, 1280, 720])):
            pushPlus(my_token, "没票了", "你妈死了" + str(time.time()))
            break

    if ld.find(ImageTemplate(IMAGES_DIR + "超鬼王/集结.png", region=[200, 300, 300, 400])):
        sleep(2)
        if ld.find(
                ImageTemplate(IMAGES_DIR + "超鬼王/易.png", region=[0, 250, 100, 350], threshold=0.8,
                              level=0)) or ld.find(
            ImageTemplate(IMAGES_DIR + "超鬼王/中.png", region=[0, 250, 100, 350], threshold=0.8, level=0)) or ld.find(
            ImageTemplate(IMAGES_DIR + "超鬼王/高.png", region=[0, 250, 100, 350], threshold=0.8, level=0)):
            ld.findAndClick(ImageTemplate(IMAGES_DIR + "超鬼王/挑战.png", region=[1000, 500, 1280, 720], threshold=0.8))
            ld.findAndClick(
                ImageTemplate(IMAGES_DIR + "超鬼王/挑战2.png", region=[1000, 500, 1280, 720], threshold=0.8))
        else:
            pushPlus(my_token, "发现高星鬼王", "你妈死了" + str(time.time()))
            break

    if ld.findAndClick(ImageTemplate(IMAGES_DIR + "超鬼王/关闭.png", region=[800, 100, 1000, 250])):
        pushPlus(my_token, "脚本该休息了", "zen你妈死了" + str(time.time()))
        # 休息10分钟继续
        sleep(600)
    sleep(1)
