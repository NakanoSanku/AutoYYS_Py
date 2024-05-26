#  协作任务实现
from pygamescript import GameScript, ImageTemplate
from loguru import logger

from src.config import IMAGES_DIR


class HelpTask:
    defaultConfig = {
        "勾协": ImageTemplate(
            templatePath=IMAGES_DIR + "/协作/勾协.png", describe="勾协标识"
        ),
        "接受": ImageTemplate(
            templatePath=IMAGES_DIR + "/协作/接受.png", describe="接受"
        ),
        "拒绝": ImageTemplate(
            templatePath=IMAGES_DIR + "/协作/拒绝.png", describe="手动按钮"
        ),
        "是否接受勾协": True
    }

    def __init__(self, device: GameScript, updateConfig=None) -> None:
        if updateConfig is None:
            updateConfig = {}
        self.device = device
        self.config = self.defaultConfig
        self.config.update(updateConfig)

    def run(self):
        self.__check()

    def __check(self):
        if self.config["是否接受勾协"] and self.device.find(self.config["勾协"]):
            self.device.findAndClick(self.config["接受"])
            logger.info("成功接受勾协")
        else:
            self.device.findAndClick(self.config["拒绝"])

    def __str__(self) -> str:
        return "协作任务"
