#  道馆逻辑实现
import loguru
from pygamescript import GameScript, ImageTemplate, MultiColorsTemplate

from ..config import IMAGES_DIR
from .ready import ReadyTask
from .settle import SETTLE_FAIL, SETTLE_REWARD, SETTLE_WIN, SettleTask


class Dogoate:
    defaultConfig = {
        "挑战": ImageTemplate(
            templatePath=IMAGES_DIR + "/道馆/挑战.png", describe="挑战图标",
            region=[944, 385, 1279, 719]
        ),
        "庭院标识": MultiColorsTemplate(firstColor="#d5ad58",
                                        colors=[[0, 0, "#d5ad58"], [23, 5, "#e7cba4"], [13, 20, "#cc9543"],
                                                [194, 5, "#ee573c"], [183, 8, "#d61f0f"], [348, 2, "#ff8938"],
                                                [348, 11, "#f2622e"], [344, -7, "#ea7532"]],
                                        region=[467, 3, 1042, 72],
                                        threshold=15)
    }

    def __init__(self, device: GameScript, updateConfig=None) -> None:
        if updateConfig is None:
            updateConfig = {}
        self.device = device
        self.done = False
        self.config = self.defaultConfig
        self.config.update(updateConfig)
        # 准备阶段任务初始化
        self.readyTask = ReadyTask(self.device)
        # 结算阶段任务初始化
        self.settleTaskReward = SettleTask(self.device, SETTLE_REWARD)
        self.settleTaskWin = SettleTask(self.device, SETTLE_WIN, isColor=True)
        self.settleTaskFail = SettleTask(self.device, SETTLE_FAIL, isColor=True)

    def run(self):
        self.device.findAndClick(self.config['挑战'], isColor=True)
        if self.device.find(self.config["庭院标识"]):
            loguru.logger.info("道馆结束")
            loguru.logger.info("已经回到庭院")
            self.done = True
            return
        # 准备阶段
        self.readyTask.run()
        # 结算阶段
        self.settleTaskFail.run()
        self.settleTaskReward.run()
        self.settleTaskWin.run()

    def __str__(self) -> str:
        return "道馆"
