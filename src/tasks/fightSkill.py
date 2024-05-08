#  通用单人战斗实现
from pygamescript import GameScript, ImageTemplate
from loguru import logger

from ..config import IMAGES_DIR
from .settle import SETTLE_VIEW, SettleTask,SETTLE_WIN


class FightSkill:
    defaultConfig = {
        "挑战按钮": ImageTemplate(
            templatePath=IMAGES_DIR + "/斗技/挑战.png", describe="斗技挑战按钮", threshold=0.8,
            region=[1120, 540, 1280, 720]
        ),
        "自动上阵": ImageTemplate(
            templatePath=IMAGES_DIR + "/斗技/自动上阵.png", describe="自动上阵按钮",
            region=[0, 100, 100, 200]
        ),
        "手动": ImageTemplate(
            templatePath=IMAGES_DIR + "/斗技/手动.png", describe="手动按钮",
            region=[0, 600, 100, 700]
        )
    }

    def __init__(self, device: GameScript, times: int, updateConfig=None) -> None:
        if updateConfig is None:
            updateConfig = {}
        self.device = device
        self.times = times
        self.runTimes = 0
        self.done = False
        self.config = self.defaultConfig
        self.config.update(updateConfig)
        # 结算阶段任务初始化
        self.settleTaskView = SettleTask(self.device, SETTLE_VIEW)
        self.settleTaskWin = SettleTask(self.device, SETTLE_WIN)

    def run(self):
        # 判断任务次数是否已经符合条件
        if self.runTimes >= self.times:
            self.done = True
            return
        # 点击挑战阶段
        self.__fight()
        # 自动上阵阶段
        self.__autoDeploy()
        # 手动战斗转自动阶段
        self.__hand2auto()
        # 结算阶段
        if self.settleTaskView.run():
            self.runTimes += 1
        self.settleTaskWin.run()

    def __fight(self):
        self.device.findAndClick(self.config["挑战按钮"])

    def __autoDeploy(self):
        self.device.findAndClick(self.config["自动上阵"])

    def __hand2auto(self):
        self.device.findAndClick(self.config["手动"])

    def __str__(self) -> str:
        return "单人挑战任务<{}/{}>".format(self.runTimes, self.times)
