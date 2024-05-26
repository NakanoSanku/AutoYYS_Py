# 通用场景切换实现
import time

import loguru
from pygamescript import GameScript, ImageTemplate, MultiColorsTemplate, Template
from loguru import logger

from src.config import IMAGES_DIR


class EnterScene:
    defaultConfig = {
        "回退到庭院": {
            "动作库": {
                "确认1": ImageTemplate(
                    templatePath=IMAGES_DIR + "/场景切换/回退庭院/确认1.png", describe="确认按钮1",
                    region=[622, 341, 906, 512]
                ),
                "确认2": ImageTemplate(
                    templatePath=IMAGES_DIR + "/场景切换/回退庭院/确认2.png", describe="确认按钮2",
                    region=[637, 333, 930, 469]
                ),
                "确认3": ImageTemplate(
                    templatePath=IMAGES_DIR + "/场景切换/回退庭院/确认3.png", describe="确认按钮3",
                    region=[643, 341, 971, 509]
                ),
                "关闭1": ImageTemplate(
                    templatePath=IMAGES_DIR + "/场景切换/回退庭院/关闭1.png", describe="关闭1",
                    region=[568, 2, 1279, 465]
                ),
                "关闭2": ImageTemplate(
                    templatePath=IMAGES_DIR + "/场景切换/回退庭院/关闭2.png", describe="关闭2",
                    region=[568, 2, 1279, 465]
                ),
                "返回1": ImageTemplate(
                    templatePath=IMAGES_DIR + "/场景切换/回退庭院/返回1.png", describe="返回按钮1",
                    region=[0, 0, 311, 221]
                ),
                "返回2": ImageTemplate(
                    templatePath=IMAGES_DIR + "/场景切换/回退庭院/返回2.png", describe="返回按钮2",
                    region=[0, 0, 311, 221]
                ),
                "返回3": ImageTemplate(
                    templatePath=IMAGES_DIR + "/场景切换/回退庭院/返回3.png", describe="返回按钮3",
                    region=[0, 0, 311, 221]
                ),
                "返回4": ImageTemplate(
                    templatePath=IMAGES_DIR + "/场景切换/回退庭院/返回4.png", describe="返回按钮4",
                    region=[0, 0, 311, 221]
                ),
                "返回5": ImageTemplate(
                    templatePath=IMAGES_DIR + "/场景切换/回退庭院/返回5.png", describe="返回按钮5",
                    region=[0, 0, 311, 221]
                ),
                "退出1": ImageTemplate(
                    templatePath=IMAGES_DIR + "/场景切换/回退庭院/退出1.png", describe="退出按钮1",
                    region=[0, 0, 311, 221]
                ),
                "庭院": ImageTemplate(
                    templatePath=IMAGES_DIR + "/场景切换/回退庭院/庭院.png", describe="庭院",
                    region=[988, 181, 1146, 389]
                ),
            },
            "成功标志": MultiColorsTemplate("#dcb653", [[10, -3, "#e7c971"], [20, 1, "#efcc7a"], [24, 15, "#d09e55"],
                                                        [13, 18, "#c2934b"], [191, 8, "#f95d47"], [186, 20, "#cdb696"],
                                                        [195, 10, "#ef452c"], [350, 5, "#cb440c"], [359, 17, "#cf5331"],
                                                        [357, 21, "#20231a"], [355, 4, "#ff873f"]],
                                            region=[463, 6, 1077, 98],
                                            threshold=26)
        },
        "进入结界": {
            "动作库": {
                "阴阳寮": ImageTemplate(templatePath=IMAGES_DIR + "/场景切换/进入阴阳寮/阴阳寮.png",
                                        region=[510, 576, 641, 699]),
                "结界": ImageTemplate(templatePath=IMAGES_DIR + "/场景切换/进入阴阳寮/进入结界/结界.png",
                                      region=[1038, 596, 1161, 716])
            },
            "成功标志": MultiColorsTemplate("#362b2d", [[-2, -7, "#292421"], [1, -12, "#332b2b"], [7, -13, "#292421"],
                                                        [-2, -18, "#d6b28c"], [9, -14, "#292021"], [44, -14, "#4c403e"],
                                                        [43, -18, "#ceaa8c"], [55, -12, "#312829"], [55, 0, "#382c2d"]]
                                            , region=[845, 470, 1135, 618], threshold=26)
        },
        "进入逢魔之时": {
            "动作库": {
                "町中": ImageTemplate(templatePath=IMAGES_DIR + "/场景切换/进入町中/町中.png",
                                      region=[668, 226, 870, 379]),
                "逢魔之时": ImageTemplate(templatePath=IMAGES_DIR + "/场景切换/进入町中/逢魔之时/逢魔之时.png",
                                          region=[567, 122, 701, 259]),
            },
            "成功标志": ImageTemplate(templatePath=IMAGES_DIR + "/场景切换/进入町中/逢魔之时/指南针.png",
                                      region=[2, 609, 105, 719]),
        },
        "进入地域鬼王": {
            "动作库": {
                "地域鬼王": ImageTemplate(templatePath=IMAGES_DIR + "/场景切换/进入地域鬼王/地域鬼王.png",
                                          region=[582, 599, 791, 719]),
                "探索": ImageTemplate(templatePath=IMAGES_DIR + "/场景切换/进入地域鬼王/探索.png",
                                      region=[621, 106, 755, 235]),
            },
            "成功标志": ImageTemplate(templatePath=IMAGES_DIR + "/场景切换/进入地域鬼王/今日挑战.png",
                                      region=[8, 325, 161, 476]),
        },
        "进入组队": {
            "动作库": {
                "组队": ImageTemplate(templatePath=IMAGES_DIR + "/场景切换/进入组队/组队.png",
                                      region=[396, 570, 525, 705])
            },
            "成功标志": ImageTemplate(templatePath=IMAGES_DIR + "/场景切换/进入组队/组队标识.png",
                                      region=[11, 6, 417, 175])
        },
        "模板": {
            "动作库": {

            },
            "成功标志": None
        }
    }

    def __init__(self, device: GameScript, actionsName: str) -> None:
        self.device = device
        self.done = False
        self.actionsName = actionsName
        self.action = self.defaultConfig[actionsName]

    def run(self):
        if not self.__enterActions(self.action["动作库"]):
            self.__successSign(self.action["成功标志"])

    def __enterActions(self, actionsTemplate: dict):
        for _, value in actionsTemplate.items():

            if self.device.findAndClick(value):
                return True

    def __successSign(self, template):
        if self.device.find(template):
            loguru.logger.info("{}".format(self.actionsName))
            self.done = True
            return

    def __str__(self):
        return "从一个庭院进入其他场景的任务集合类"
