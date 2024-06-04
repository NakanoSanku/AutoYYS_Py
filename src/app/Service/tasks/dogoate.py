#  道馆逻辑实现
import loguru
from pygamescript import GameScript, ImageColorTemplate, MultiColorsTemplate

from src.config import IMAGES_DIR
from .ready import ReadyTask
from .settle import SETTLE_FAIL, SETTLE_REWARD, SETTLE_WIN, SettleTask


class Dogoate:
    defaultConfig = {
        "挑战": ImageColorTemplate(
            template_path=IMAGES_DIR + "/道馆/挑战.jpg",
            describe="挑战图标",
            region=[944, 385, 1279, 719],
        ),
        "庭院标识": MultiColorsTemplate(
            first_color="#d5ad58",
            colors=[
                [0, 0, "#d5ad58"],
                [23, 5, "#e7cba4"],
                [13, 20, "#cc9543"],
                [194, 5, "#ee573c"],
                [183, 8, "#d61f0f"],
                [348, 2, "#ff8938"],
                [348, 11, "#f2622e"],
                [344, -7, "#ea7532"],
            ],
            region=[467, 3, 1042, 72],
            threshold=15,
        ),
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
        self.settleTaskWin = SettleTask(self.device, SETTLE_WIN)
        self.settleTaskFail = SettleTask(self.device, SETTLE_FAIL)

    def run(self):
        self.device.find_and_click(self.config["挑战"])
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
