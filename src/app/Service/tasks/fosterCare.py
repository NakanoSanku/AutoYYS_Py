# 寄养式神实现
import random
import time

import loguru
from pygamescript import GameScript, ImageTemplate, MultiColorsTemplate, algo
from loguru import logger

from src.config import IMAGES_DIR


class EnterScene:
    defaultConfig = {
        "式神育成": ImageTemplate(templatePath=IMAGES_DIR + "/寄养/式神育成.png", region=[596, 271, 745, 416]),
        "加号": ImageTemplate(templatePath=IMAGES_DIR + "/寄养/加号.png", region=[1110, 29, 1251, 154]),
        "跨区": ImageTemplate(templatePath=IMAGES_DIR + "/寄养/跨区.png", region=[325, 65, 494, 186]),
        "好友": ImageTemplate(templatePath=IMAGES_DIR + "/寄养/好友.png", region=[195, 76, 345, 177]),
        "下拉绳头": ImageTemplate(templatePath=IMAGES_DIR + "/寄养/下拉绳头.png", region=[132, 133, 300, 593]),
        "下拉起点范围": [181, 184, 200, 204],
        "下拉终点范围": [177, 521, 203, 543],
        "下拉持续时间范围": [300, 500],
        "下拉延迟": 1
    }

    def __init__(self, device: GameScript, updateConfig=None) -> None:
        if updateConfig is None:
            updateConfig = {}
        self.device = device
        self.done = False
        self.config = self.defaultConfig
        self.config.update(updateConfig)

    def run(self):
        self.device.findAndClick(self.config["式神育成"])
        self.device.findAndClick(self.config["加号"])
        if self.device.find(self.config["下拉绳头"]):
            startX, startY = algo.RandomPointGenerate.normalDistribution(self.config["下拉起点范围"])
            endX, endY = algo.RandomPointGenerate.normalDistribution(self.config["下拉终点范围"])
            duration = random.randint(self.config["下拉持续时间范围"][0], self.config["下拉持续时间范围"][1])
            self.device.curveSwipe(startX, startY, endX, endY, duration)
            time.sleep(self.config["下拉延迟"])
        self.device.findAndClick(self.config["跨区"])
        if self.device.find(self.config["下拉绳头"]):
            startX, startY = algo.RandomPointGenerate.normalDistribution(self.config["下拉起点范围"])
            endX, endY = algo.RandomPointGenerate.normalDistribution(self.config["下拉终点范围"])
            duration = random.randint(self.config["下拉持续时间范围"][0], self.config["下拉持续时间范围"][1])
            self.device.curveSwipe(startX, startY, endX, endY, duration)
            time.sleep(self.config["下拉延迟"])
        self.device.findAndClick(self.config["好友"])

        pass

    def __str__(self):
        return "从一个庭院进入其他场景的任务集合类"
