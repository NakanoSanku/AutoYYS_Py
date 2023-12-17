import time

from loguru import logger

from src.tasks.base.settle.task import settleReward
from src.tasks.qiLing.assets import *


def qiLingNameSet(name):
    if name == "镇墓兽":
        return QILING_TOMB_GUARD
    if name == "火灵":
        return QILING_FIRE_SPIRIT
    if name == "茨球":
        return QILING_BALL
    if name == "小黑":
        return QILING_BLACK
    raise ValueError("No Correspondence QiLing!")


def qiLing(device: GameScript, times: int, name="镇墓兽"):
    QILING_NAME = qiLingNameSet(name)
    i = 0
    while i < times:
        # 选择并召唤契灵
        if device.findAndClick(QILING_NAME):
            time.sleep(1)
            if device.findAndClick(QILING_CONFIRM):
                time.sleep(10)
        # 找已召唤契灵位置，没找到则点击召唤
        if not device.findAndClick(QILING_FIRE):
            device.findAndClick(QILING_CALL)
        # 点击挑战
        device.findAndClick(QILING_FIGHT)
        # 结算
        settleReward(device)
        if device.findAndClick(QILING_CATCH_SUCCESS):
            time.sleep(15)
            i += 1
            logger.info(f'{i}次捕获成功完成')
        # 休息
        time.sleep(0.8)
