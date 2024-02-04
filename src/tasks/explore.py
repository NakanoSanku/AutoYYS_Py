# TODO: 探索功能实现
import time
import random

import loguru
from pygamescript import GameScript, ImageTemplate, algo

from src.tasks.settle import SettleTask, SETTLE_VIEW
from src.utils.ocrTemplate import (OcrTemplate)
from src.config import IMAGES_DIR

EXPLORE_CONFIG = {
    "妖": ImageTemplate(
        templatePath=IMAGES_DIR + "/探索/妖.png", region=[1077, 78, 1245, 205]
    ),
    "探索": ImageTemplate(
        templatePath=IMAGES_DIR + "/探索/探索.png", region=[845, 474, 1057, 622]
    ),
    "式神录": ImageTemplate(
        templatePath=IMAGES_DIR + "/探索/式神录.png", region=[744, 623, 885, 719]
    ),
    "小怪": ImageTemplate(
        templatePath=IMAGES_DIR + "/探索/小怪.png",
        region=[7, 152, 1273, 719],
        threshold=0.8,
    ),
    "BOSS": ImageTemplate(
        templatePath=IMAGES_DIR + "/探索/BOSS.png",
        region=[7, 152, 1273, 719],
        threshold=0.8,
    ),
    "退出": ImageTemplate(templatePath=IMAGES_DIR + "/探索/退出.png"),
    "退出_确认": ImageTemplate(templatePath=IMAGES_DIR + "/探索/退出_确认.png"),
    "宝箱": ImageTemplate(templatePath=IMAGES_DIR + "/探索/宝箱.png"),
    "粉色叉": ImageTemplate(templatePath=IMAGES_DIR + "/探索/粉色叉.png"),
    "选择章节后延迟": 1,
    "点击打怪延迟": 1,
    "滑动起点范围": [1000, 120, 1100, 120],
    "滑动终点范围": [500, 90, 600, 120],
    "滑动持续时间范围": [350, 400],
    "最大滑动次数": 5,
    "章节": "第二十八章",
}


class Explore:
    def __init__(self, device: GameScript, times: int, config=None):
        self.config = EXPLORE_CONFIG
        if config is None:
            config = {}
        self.config.update(config)
        self.device = device
        self.times = times
        self.runTimes = 0
        self.done = False
        self.settle = SettleTask(device, SETTLE_VIEW)

        self.chapterTemplate = OcrTemplate(
            text=self.config["章节"], region=[1038, 181, 1272, 682], isGary=True
        )
        self.BOSSMark = False
        self.swipeTimes = 0

    def run(self):
        # 判断任务次数是否已经符合条件
        if self.runTimes >= self.times:
            self.done = True
            return
        # 探索界面阶段
        self.__explorePageStage()
        # 选择怪阶段
        self.__findMonsterPage()
        # 其他阶段
        if self.device.findAndClick(self.config["探索"]):
            self.BOSSMark = False
        if self.settle.run():
            self.runTimes += 1
            loguru.logger.info(self)

    def __explorePageStage(self):
        if self.device.find(self.config["妖"]):
            self.device.findAndClick(self.config["宝箱"])
            time.sleep(self.config["选择章节后延迟"])
            self.device.findAndClick(self.chapterTemplate)

    def __findMonsterPage(self):
        if self.device.find(self.config["式神录"]):
            return (
                self.__exitFindMonsterPage() if self.BOSSMark else self.__findMonster()
            )

    def __findMonster(self):
        if self.device.findAndClick(self.config["BOSS"]):
            time.sleep(self.config["点击打怪延迟"])
            if not self.device.find(self.config["BOSS"]):
                self.BOSSMark = True
            return
        if not self.device.findAndClick(self.config["小怪"]):
            if self.swipeTimes == self.config["最大滑动次数"]:
                self.BOSSMark = True
                self.swipeTimes = 0
                return
            startX, startY = algo.RandomPointGenerate.normalDistribution(
                self.config["滑动起点范围"]
            )
            endX, endY = algo.RandomPointGenerate.normalDistribution(
                self.config["滑动终点范围"]
            )
            minDuration, maxDuration = self.config["滑动持续时间范围"]
            duration = random.randint(minDuration, maxDuration)
            self.device.curveSwipe(startX, startY, endX, endY, duration)
            self.swipeTimes += 1
        else:
            self.swipeTimes = 0
        time.sleep(self.config["点击打怪延迟"])

    def __exitFindMonsterPage(self):
        if not self.device.findAndClick(self.config["退出_确认"]):
            self.device.findAndClick(self.config["退出"])

    def __str__(self):
        return "探索任务<{}/{}>".format(self.runTimes, self.times)
