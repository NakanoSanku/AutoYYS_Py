# 抽厕纸功能实现
from loguru import logger
from pygamescript import GameScript, ImageTemplate

from src.config import IMAGES_DIR


class ToiletPaper:
    defaultConfig = {
        "再次召唤按钮": ImageTemplate(
            template_path=IMAGES_DIR + "/抽厕纸/再次召唤.png", describe="再次召唤按钮"
        ),
        "次数": 0
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

    def run(self):
        # 判断任务次数是否已经符合条件
        if self.runTimes >= self.times:
            self.done = True
            return
        if self.device.find_and_click(self.config["再次召唤按钮"]):
            self.runTimes += 1  # 计次
            logger.info(self)  # 日志输出任务当前状态

    def __str__(self) -> str:
        return "抽厕纸{}/{}".format(self.runTimes, self.times)
