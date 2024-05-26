#  通用单人战斗实现
import time

import loguru
from pygamescript import GameScript, ImageTemplate
from loguru import logger

from src.config import IMAGES_DIR
from .settle import SettleTask, SETTLE_REWARD, SETTLE_FAIL, SETTLE_WIN
from .ready import ReadyTask


class RegionalGhostKing:
    defaultConfig = {
        "挑战按钮": ImageTemplate(
            templatePath=IMAGES_DIR + "/地域鬼王/挑战.png", describe="地域鬼王挑战按钮"
        ),
        "今日挑战": ImageTemplate(
            templatePath=IMAGES_DIR + "/地域鬼王/今日挑战.png", describe="地域鬼王今日挑战按钮",
            region=[9, 310, 155, 479]
        ),
        "未选择": ImageTemplate(
            templatePath=IMAGES_DIR + "/地域鬼王/未选择.png", describe="未选择鬼王",
            region=[134, 349, 491, 450]
        ),
        "筛选": ImageTemplate(
            templatePath=IMAGES_DIR + "/地域鬼王/筛选.png", describe="未选择鬼王",
            region=[1084, 6, 1191, 126]
        ),
        "挑战": ImageTemplate(
            templatePath=IMAGES_DIR + "/地域鬼王/挑战.png", describe="挑战鬼王"
        ),
        "挑战鬼王按钮范围数组": [[1070, 213, 1165, 316], [1069, 368, 1167, 462], [1069, 524, 1169, 620]],
        "挑战2": ImageTemplate(
            templatePath=IMAGES_DIR + "/地域鬼王/挑战2.png", describe="挑战鬼王", region=[1045, 455, 1263, 644]
        ),
        "关闭": ImageTemplate(
            templatePath=IMAGES_DIR + "/地域鬼王/粉色叉.png", region=[1180, 6, 1271, 102]
        ),
        "今日挑战动画延迟": 1,
        "筛选动画延迟": 1,
        "挑战按钮延迟": 1,
        "结算成功延迟": 10

    }

    def __init__(self, device: GameScript, updateConfig=None) -> None:
        if updateConfig is None:
            updateConfig = {}
        self.device = device
        self.runTimes = 0
        self.done = False
        self.config = self.defaultConfig
        self.config.update(updateConfig)
        # 结算阶段任务初始化
        self.settleTaskReward = SettleTask(self.device, SETTLE_REWARD)
        self.settleTaskWin = SettleTask(self.device, SETTLE_WIN, isColor=True)
        self.settleTaskFail = SettleTask(self.device, SETTLE_FAIL, isColor=True)
        self.readyTask = ReadyTask(self.device)

    def run(self):
        if self.device.findAndClick(self.config["今日挑战"]):
            time.sleep(self.config["今日挑战动画延迟"])
            if self.device.find(self.config["今日挑战"]):
                if self.device.find(self.config["未选择"]):
                    if self.device.findAndClick(self.config["筛选"]):
                        time.sleep(self.config["筛选动画延迟"])
                        self.config["挑战"].region = self.config["挑战鬼王按钮范围数组"][self.runTimes]
                        self.device.findAndClick(self.config["挑战"])
                else:
                    loguru.logger.info("今日地域鬼王已完成")
                    self.done = True
                    return
        self.device.findAndClick(self.config['挑战2'])
        if self.settleTaskReward.run():
            self.runTimes += 1
            time.sleep(self.config["结算成功延迟"])
            loguru.logger.info("挑战成功第{}个鬼王".format(self.runTimes))
            self.device.findAndClick(self.config["关闭"])
        self.settleTaskWin.run()
        self.settleTaskFail.run()
        self.readyTask.run()

    def __str__(self) -> str:
        return "地域鬼王任务"
