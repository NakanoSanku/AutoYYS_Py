import time

import loguru
from pygamescript import GameScript, ImageTemplate
from loguru import logger

from ..config import IMAGES_DIR
from .settle import SETTLE_VIEW, SettleTask
from .ready import ReadyTask


class DevilTime:
    defaultConfig = {
        "灵魂": ImageTemplate(
            templatePath=IMAGES_DIR + "/逢魔之时/灵魂.png", describe="灵魂",

        ),
        "现世逢魔": ImageTemplate(
            templatePath=IMAGES_DIR + "/逢魔之时/现世逢魔.png", describe="现世逢魔",
            region=[1082, 541, 1279, 719]
        ),
        "奖励": ImageTemplate(
            templatePath=IMAGES_DIR + "/逢魔之时/奖励.png", describe="奖励", threshold=0.8,
            region=[1181, 186, 1279, 281]
        ),
        "已领取": ImageTemplate(
            templatePath=IMAGES_DIR + "/逢魔之时/已领取.png", describe="已领取",
            region=[1181, 186, 1279, 281]
        ),
        # TODO: 获得奖励的范围
        "获得奖励": ImageTemplate(
            templatePath=IMAGES_DIR + "/逢魔之时/获得奖励.png",
        ),
        "现世逢魔延迟": 3,
        "首领": ImageTemplate(
            templatePath=IMAGES_DIR + "/逢魔之时/首领.png", describe="首领",
            region=[967, 613, 1087, 719]
        ),
        "逢魔极": ImageTemplate(
            templatePath=IMAGES_DIR + "/逢魔之时/逢魔极.png", describe="逢魔极",
            region=[855, 615, 1002, 719]
        ),
        "集结": ImageTemplate(
            templatePath=IMAGES_DIR + "/逢魔之时/集结.png", describe="集结", threshold=0.8
        ),
        "集结挑战": ImageTemplate(
            templatePath=IMAGES_DIR + "/逢魔之时/集结挑战.png", describe="集结挑战", region=[991, 512, 1252, 710]
        ),
        "关闭": ImageTemplate(
            templatePath=IMAGES_DIR + "/逢魔之时/关闭.png", describe="关闭", region=[1065, 29, 1197, 147]
        ),
        "首领类型": "首领",
        "搜索首领延迟": 3,
        "集结挑战延迟": 3,
        "搜索首领冷却时间": 5
    }

    def __init__(self, device: GameScript, updateConfig=None) -> None:
        if updateConfig is None:
            updateConfig = {}
        self.device = device
        self.done = False
        self.taskOneDone = False
        self.taskTwoDone = False
        self.config = self.defaultConfig
        self.config.update(updateConfig)
        self.settleTask = SettleTask(self.device, self.config["获得奖励"])
        self.settleTaskView = SettleTask(self.device, SETTLE_VIEW)
        self.readyTask = ReadyTask(self.device)

    def run(self):
        # 点四下并领取奖励
        self.taskOne()
        # 逢魔首领之战
        self.taskTwo()
        if self.taskTwoDone and self.taskOneDone:
            self.done = True

    def taskOne(self):
        if self.taskOneDone:
            return
        if self.device.find(self.config["灵魂"]):
            self.device.findAndClick(self.config['现世逢魔'])
            time.sleep(self.config['现世逢魔延迟'])
        else:
            if self.device.find(self.config['已领取'], isColor=True):
                self.taskOneDone = True
                loguru.logger.info("————今日四次现世逢魔已完成！————")
            else:
                self.device.findAndClick(self.config["奖励"])
            self.settleTask.run()

    def taskTwo(self):
        if self.taskTwoDone:
            return
        self.readyTask.run()
        if self.settleTaskView.run():
            self.taskTwoDone = True
        if not self.device.findAndClick(self.config["集结"]):
            if self.device.findAndClick(self.config["集结挑战"]):
                time.sleep(self.config["集结挑战延迟"])
                if self.device.find(self.config["集结挑战"]):
                    self.device.findAndClick(self.config["关闭"])
            time.sleep(self.config["搜索首领冷却时间"])
            if self.device.findAndClick(self.config[self.config["首领类型"]]):
                time.sleep(self.config['搜索首领延迟'])

    def __str__(self) -> str:
        return "逢魔之时"
