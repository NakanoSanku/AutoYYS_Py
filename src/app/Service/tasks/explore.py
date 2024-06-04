import random
import time

import loguru
from pygamescript import GameScript, ImageTemplate, algo

from src.config import IMAGES_DIR
from .settle import SettleTask, SETTLE_VIEW


class Explore:
    defaultConfig = {
        "探索界面标识": ImageTemplate(
            template_path=IMAGES_DIR + "/探索/突破票.png", region=[600, 0, 750, 150]
        ),
        "探索": ImageTemplate(
            template_path=IMAGES_DIR + "/探索/探索.png", region=[845, 474, 1057, 622]
        ),
        "式神录": ImageTemplate(
            template_path=IMAGES_DIR + "/探索/式神录.png", region=[744, 623, 885, 719]
        ),
        "小怪": ImageTemplate(
            template_path=IMAGES_DIR + "/探索/小怪.png",
            region=[7, 152, 1273, 719],
            threshold=0.75,
        ),
        "BOSS": ImageTemplate(
            template_path=IMAGES_DIR + "/探索/BOSS.png",
            region=[7, 152, 1273, 719],
            threshold=0.8,
        ),
        "关闭探索界面": ImageTemplate(template_path=IMAGES_DIR + "/探索/粉色叉.png", region=[1000, 100, 1100, 200]),
        "退出": ImageTemplate(template_path=IMAGES_DIR + "/探索/退出.png", region=[13, 25, 110, 117]),
        "退出_确认": ImageTemplate(template_path=IMAGES_DIR + "/探索/退出_确认.png", region=[666, 361, 903, 456]),
        "宝箱": ImageTemplate(template_path=IMAGES_DIR + "/探索/宝箱.png"),
        "章节": ImageTemplate(template_path=IMAGES_DIR + "/探索/第二十八章.png", region=[1038, 181, 1272, 682]),
        "选择章节后延迟": 1,
        "点击打怪延迟": 0.5,
        "滑动起点范围": [1000, 120, 1100, 120],
        "滑动终点范围": [500, 90, 600, 120],
        "滑动持续时间范围": [350, 400],
        "最大滑动次数": 5,
        "次数": 0
    }

    def __init__(self, device: GameScript, updateConfig=None):
        if updateConfig is None:
            updateConfig = {}
        self.device = device
        self.runTimes = 0
        self.done = False
        self.settle = SettleTask(device, SETTLE_VIEW)
        self.config = self.defaultConfig
        self.config.update(updateConfig)
        self.BOSSMark = False
        self.swipeTimes = 0
        self.times = self.config["次数"]

    def run(self):
        #
        # 探索界面阶段
        self.__explorePageStage()
        # 选择怪阶段
        self.__findMonsterPageStage()
        # 具体章节阶段
        self.__exploreChapterPageStage()
        # 结算阶段
        if self.settle.run():
            self.runTimes += 1
            loguru.logger.info(self)

    def __explorePageStage(self):
        if self.device.find(self.config["探索界面标识"]):
            # 判断任务次数是否已经符合条件
            if self.runTimes >= self.times:
                if self.device.find(self.config["探索界面标识"]):
                    self.done = True
                    return
            self.device.find_and_click(self.config["宝箱"])
            time.sleep(self.config["选择章节后延迟"])
            self.device.find_and_click(self.config["章节"])

    def __findMonsterPageStage(self):
        # TODO: 做一个没狗粮自动换的逻辑
        if self.device.find(self.config["式神录"]):
            return (
                self.__exitFindMonsterPage() if self.BOSSMark else self.__findMonster()
            )

    def __exploreChapterPageStage(self):
        # 如果战斗次数已经完成就关闭界面
        if self.runTimes >= self.times:
            self.device.find_and_click(self.config["关闭探索界面"])
            return
        # 点击探索
        if self.device.find_and_click(self.config["探索"]):
            self.BOSSMark = False

    def __findMonster(self):
        if self.device.find_and_click(self.config["BOSS"]):
            time.sleep(self.config["点击打怪延迟"])
            if not self.device.find(self.config["BOSS"]):
                self.BOSSMark = True
            return
        if not self.device.find_and_click(self.config["小怪"]):
            if self.swipeTimes == self.config["最大滑动次数"]:
                self.BOSSMark = True
                self.swipeTimes = 0
                return
            startX, startY = algo.RandomPointGenerate.normal_distribution(
                self.config["滑动起点范围"]
            )
            endX, endY = algo.RandomPointGenerate.normal_distribution(
                self.config["滑动终点范围"]
            )
            minDuration, maxDuration = self.config["滑动持续时间范围"]
            duration = random.randint(minDuration, maxDuration)
            self.device.curve_swipe(startX, startY, endX, endY, duration)
            self.swipeTimes += 1
        else:
            self.swipeTimes = 0
        time.sleep(self.config["点击打怪延迟"])

    def __exitFindMonsterPage(self):
        if not self.device.find_and_click(self.config["退出_确认"]):
            self.device.find_and_click(self.config["退出"])

    def __str__(self):
        return "探索任务<{}/{}>".format(self.runTimes, self.times)
