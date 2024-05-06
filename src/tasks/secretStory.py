#  秘闻竞速任务实现 TODO: 完成标识待完善
import loguru
from pygamescript import GameScript, ImageTemplate
from loguru import logger

from ..config import IMAGES_DIR
from .ready import ReadyTask
from .settle import SETTLE_FAIL, SETTLE_REWARD, SETTLE_WIN, SettleTask


class SecretStory:
    defaultConfig = {
        "秘闻挑战按钮": ImageTemplate(
            templatePath=IMAGES_DIR + "/秘闻竞速/挑战.png", describe="秘闻挑战按钮"
        ),
        "尚未通关": ImageTemplate(
            templatePath=IMAGES_DIR + "/秘闻竞速/尚未通关.png", describe="尚未通关标识"
        ),
        "失败后是否再次挑战": False
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
        self.settleTaskReward = SettleTask(
            self.device, SETTLE_REWARD)
        self.settleTaskWin = SettleTask(
            self.device,
            SETTLE_WIN,
            isColor=True,
        )
        self.settleTaskFail = SettleTask(
            self.device,
            SETTLE_FAIL,
            isColor=True,
            fightAgain=self.config["失败后是否再次挑战"],
        )  # 失败后自动再次挑战

    def run(self):
        self.__fight()
        self.readyTask.run()
        self.settleTaskFail.run()
        self.settleTaskWin.run()
        self.settleTaskReward.run()

    def __fight(self):
        result = self.device.find(self.config['秘闻挑战按钮'])
        if result:
            if self.device.find(self.config['尚未通关']):
                self.device.rangeRandomClick(result)
            else:
                loguru.logger.info("已通关完成")
                self.done = True

    def __str__(self) -> str:
        return "协作任务"
