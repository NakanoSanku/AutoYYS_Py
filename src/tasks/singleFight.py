# 通用单人战斗实现
from pygamescript import GameScript, ImageTemplate
from loguru import logger

from ..config import IMAGES_DIR
from .ready import ReadyTask
from .settle import SETTLE_FAIL, SETTLE_REWARD, SETTLE_WIN, SettleTask


class SingleFight:
    defaultConfig = {
        "挑战按钮": ImageTemplate(
            templatePath=IMAGES_DIR + "/单人战斗/挑战.png", describe="通用类型的单人战斗图标"
        ),
        "改变预设": False,
        "预设分组": None,
        "预设序号": None,
        "失败后是否再次挑战": False,
        "胜利结算数组": [[10, 100, 120, 550], [1150, 50, 1280, 720]],
        "失败结算数组": [[10, 100, 120, 550], [1150, 50, 1280, 720]],
        "奖励结算数组": [[10, 100, 120, 550], [1150, 50, 1280, 720]],
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
        # 准备阶段任务初始化
        self.readyTask = ReadyTask(
            self.device,
            isChangePreset=self.config["改变预设"],
            presetGroup=self.config["预设分组"],
            presetIndex=self.config["预设序号"],
        )
        # 结算阶段任务初始化
        self.settleTaskReward = SettleTask(
            self.device, SETTLE_REWARD, settleResultList=self.config["奖励结算数组"]
        )
        self.settleTaskWin = SettleTask(
            self.device,
            SETTLE_WIN,
            isColor=True,
            settleResultList=self.config["胜利结算数组"],
        )
        self.settleTaskFail = SettleTask(
            self.device,
            SETTLE_FAIL,
            isColor=True,
            fightAgain=self.config["失败后是否再次挑战"],
            settleResultList=self.config["失败结算数组"],
        )  # 失败后自动再次挑战

    def run(self):
        # 判断任务次数是否已经符合条件
        if self.runTimes >= self.times:
            self.done = True
            return
        # 点击挑战阶段
        self.__fight()
        # 准备阶段
        self.readyTask.run()
        # 结算阶段
        self.settleTaskFail.run()
        self.settleTaskWin.run()
        if self.settleTaskReward.run():
            self.runTimes += 1  # 战斗计次
            logger.info(self)  # 日志输出任务当前状态

    def __fight(self):
        self.device.findAndClick(self.config["挑战按钮"])

    def __str__(self) -> str:
        return "单人挑战任务<{}/{}>".format(self.runTimes, self.times)
