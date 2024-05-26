# 通用组队战斗实现
from pygamescript import GameScript, ImageTemplate, MultiColorsTemplate
from loguru import logger

from src.config import IMAGES_DIR
from .ready import ReadyTask
from .settle import SETTLE_FAIL, SETTLE_VIEW, SettleTask


class TeamFight:
    defaultConfig = {
        "挑战按钮": ImageTemplate(
            templatePath=IMAGES_DIR + "/组队战斗/挑战.png", describe="通用类型的组队战斗挑战图标"
        ),
        "3P": MultiColorsTemplate(
            firstColor="#fffffe",
            colors=[
                [9, 0, "#fffffe"],
                [17, -2, "#fffffe"],
                [33, -1, "#fffffe"],
                [40, 0, "#fffffd"],
                [17, -25, "#fffcd7"],
                [18, -17, "#fffef6"],
                [21, -1, "#ffffff"],
                [19, 22, "#fffffa"],
            ],
            describe="组队第三人",
            region=[1017, 178, 1153, 319],
            threshold=4,
        ),
        "是否失败后是否再次挑战": False,
        "视图结算数组": [[10, 100, 120, 420], [1150, 50, 1280, 720]],
        "是否为队长": False,
        "是否3P": False,
        "次数":0
    }

    def __init__(self, device: GameScript, updateConfig=None) -> None:
        if updateConfig is None:
            updateConfig = {}
        self.device = device
        self.runTimes = 0
        self.done = False
        self.config = self.defaultConfig
        self.config.update(updateConfig)
        self.times = self.config["次数"]
        # 准备阶段任务初始化
        self.readyTask = ReadyTask(self.device)
        # 结算阶段任务初始化
        self.settleTaskView = SettleTask(self.device, SETTLE_VIEW)
        self.settleTaskFail = SettleTask(
            self.device, SETTLE_FAIL, isColor=True, fightAgain=self.config["失败后是否再次挑战"])  # 失败后自动再次挑战

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
        if self.settleTaskView.run():
            self.runTimes += 1  # 战斗计次
            logger.info(self)  # 日志输出任务当前状态

    def __fight(self):
        if self.config["是否为队长"]:
            # 判断当前是否在组队界面且有队员入队
            result = self.device.find(template=self.config["挑战按钮"], isColor=True)
            if result:
                # 三人组队逻辑
                if not self.config["是否3P"] or not self.device.find(
                        template=self.config["3P"]
                ):
                    self.device.rangeRandomClick(result)

    def __str__(self) -> str:
        return "组队挑战任务<{}——{}/{}>".format(
            "队长" if self.config["是否为队长"] else "队员", self.runTimes, self.times
        )
