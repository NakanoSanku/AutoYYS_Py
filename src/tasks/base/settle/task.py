import random
import time

from src.tasks.base.settle.assets import *


def settle(device: GameScript, template: Template, settleResultList=None, isColor=False, colorThreshold=4):
    if settleResultList is None:
        settleResultList = [[10, 100, 120, 550], [1150, 50, 1280, 720]]
    res = None
    p = device.find(template, isColor=isColor, colorThreshold=colorThreshold)
    if p:
        res = p
        while device.findAndClick(template,
                                  result=settleResultList[random.randint(0, len(settleResultList) - 1)],
                                  isColor=isColor,
                                  colorThreshold=colorThreshold):
            time.sleep(0.05)
    return res


def settleWin(device: GameScript, settleResultList=None):
    if settleResultList is None:
        settleResultList = [[10, 100, 120, 550], [1150, 50, 1280, 720]]
    return settle(device, SETTLE_WIN, settleResultList, isColor=True, colorThreshold=15)


def settleView(device: GameScript, settleResultList=None):
    if settleResultList is None:
        settleResultList = [[10, 100, 120, 550], [1150, 50, 1280, 720]]

    return settle(device, SETTLE_VIEW, settleResultList)


def settleFail(device: GameScript, settleResultList=None):
    if settleResultList is None:
        settleResultList = [[10, 100, 120, 550], [1150, 50, 1280, 720]]
    return settle(device, SETTLE_FAIL, settleResultList, isColor=True, colorThreshold=15)


def settleReward(device: GameScript, settleResultList=None):
    if settleResultList is None:
        settleResultList = [[10, 100, 120, 550], [1150, 50, 1280, 720]]
    return settle(device, SETTLE_REWARD, settleResultList)
