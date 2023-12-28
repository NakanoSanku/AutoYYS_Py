import time

from loguru import logger

from src.tasks.base.baseTask import BaseTask
from src.tasks.base.settle.task import settleReward, SettleTask
from src.tasks.qiLing.assets import *


class QiLingTask(BaseTask):
    UNDEFINED_PAGE = -1

    def __init__(self, device: GameScript, times: int, name="镇墓兽") -> None:
        self.device = device
        self.times = times
        self.name = name
        self.runTimes = 0
        self.settleReward = SettleTask(device, SettleTask.SETTLE_REWARD_TPYE)
        self.QILING_NAME = qiLingNameSet(name)
        self.done = False
        self.page = QiLingTask.UNDEFINED_PAGE

    def __selectPage(self):
        self.page = QiLingTask.UNDEFINED_PAGE

    def run(self):
        if self.done:
            return
        if self.runTimes >= self.times:
            self.done = True
            return
        # 选择并召唤契灵
        if self.device.findAndClick(self.QILING_NAME):
            time.sleep(1)
            if self.device.findAndClick(QILING_CONFIRM):
                time.sleep(10)
        # 找已召唤契灵位置，没找到则点击召唤
        if not self.device.findAndClick(QILING_FIRE):
            self.device.findAndClick(QILING_CALL)
        # 点击挑战
        self.device.findAndClick(QILING_FIGHT)
        # 结算
        self.settleReward.run()
        if self.device.findAndClick(QILING_CATCH_SUCCESS):
            time.sleep(15)
            self.runTimes += 1
            logger.info(f'{self.runTimes}次捕获成功完成')

    def __str__(self):
        return f"QiLingTask: {self.name}"


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
