import time

import loguru
from pygamescript import GameScript, ImageTemplate
from .ready import ReadyTask
from .settle import SettleTask
from src.config import IMAGES_DIR, SCREEN_HEIGHT
from src.utils.ocrTemplate import OcrTemplate


class SixStreet:
    defaultConfig = {
        # 开启六道界面
        "攻略": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/攻略.png", region=[5, 3, 567, 184]
        ),
        "开启": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/开启.png", region=[1086, 540, 1257, 718]
        ),
        "确定": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/确定.png", region=[1086, 540, 1257, 718]
        ),
        "开启_2": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/开启_2.png", region=[1105, 546, 1271, 718]
        ),
        # BUFF选择
        "BUFF选择页面": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/BUFF_选择页面.png",
            region=[1086, 3, 1179, 86],
            describe="BUFF选择页面",
        ),
        "选择": OcrTemplate(text="选择", isGary=True),
        # 岛屿选择
        "混沌": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/混沌.png",
            threshold=0.85,
            region=[1, 261, 1268, 594],
        ),
        "宁息": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/宁息.png",
            threshold=0.85,
            region=[1, 261, 1268, 594],
        ),
        "鏖战": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/鏖战.png",
            threshold=0.85,
            region=[1, 261, 1268, 594],
        ),
        "星": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/星.png",
            threshold=0.85,
            region=[1, 261, 1268, 594],
        ),
        "神秘": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/神秘.png",
            threshold=0.85,
            region=[1, 261, 1268, 594],
        ),
        "岛屿页面": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/岛屿页面.png", region=[218, 8, 306, 88]
        ),
        # 混沌之屿
        "混沌之屿": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/混沌之岛.png", region=[66, 1, 281, 76]
        ),
        "精英": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/精英.png", region=[605, 197, 660, 254]
        ),
        # 宝箱情况
        "混沌_离开": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/离开.png", region=[1110, 558, 1275, 718]
        ),
        # 战斗岛屿
        "鏖战之屿": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/鏖战之屿.png", region=[66, 1, 281, 76]
        ),
        "普通_鏖战之屿": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/普通.png",
            region=[652, 198, 998, 449],
            threshold=0.8,
        ),
        # 神秘岛屿
        "神秘之屿": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/神秘之岛.png", region=[66, 1, 281, 76]
        ),
        # 背包仿造情况
        "背包仿造": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/背包仿造.png", region=[804, 36, 975, 105]
        ),
        "仿造": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/仿造.png",
            region=[1126, 566, 1271, 719],
            threshold=0.85,
        ),
        "仿造_柔风5级": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/仿造_柔风5级.png", region=[701, 114, 987, 336]
        ),
        "仿造_柔风位置": [823, 174, 908, 262],
        "仿造_确定": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/仿造_确认.png", region=[605, 379, 996, 539]
        ),
        # 技能转换情况
        "技能转换": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/技能转换.png", region=[804, 36, 975, 105]
        ),
        "退出岛屿": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/退出岛屿.png", region=[1, 2, 176, 130]
        ),
        # 星之岛屿
        "星之屿": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/星之岛.png", region=[66, 1, 281, 76]
        ),
        "普通_星之屿": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/普通.png",
            region=[352, 175, 502, 281],
            threshold=0.8,
        ),
        # 宁息之屿
        "宁息之屿": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/宁息之岛.png", region=[66, 1, 281, 76]
        ),
        "宁息_离开": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/宁息_离开.png",
            region=[1000, 450, 1280, 720],
            threshold=0.85,
        ),
        # 通用挑战
        "通用挑战": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/挑战.png", region=[1019, 496, 1268, 716]
        ),
        # 结算铃铛
        "结算铃铛": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/结算铃铛.png", region=[429, 155, 872, 549]
        ),
        "结算击败": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/结算击败.png",
            region=[68, 321, 519, 680],
            threshold=0.8,
        ),
        # 通用
        "通用确定": OcrTemplate(text="确定", isGary=True),
        "唤息": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/唤息.png", region=[1050, 534, 1271, 719]
        ),
        "BUFF刷新": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/BUFF刷新.png", region=[1128, 573, 1279, 719]
        ),
        "铃铛为0": ImageTemplate(
            templatePath=IMAGES_DIR + "/六道/铃铛为0.png", region=[1072, 1, 1276, 109]
        ),
        "岛屿动画延迟": 0.5,
        "BUFF选择延迟": 0.5,
        "进入岛屿多少次后刷新技能": 10,
        "BUFF选择优先列表": ["柔风抱暖", "万相之赐"],
        "岛屿选择优先列表": ["混沌", "鏖战", "神秘", "星", "宁息"],
        "次数": 0
    }

    def __init__(self, device: GameScript, updateConfig=None) -> None:
        if updateConfig is None:
            updateConfig = {}
        self.done = False
        self.device = device

        self.runTimes = 0
        self.config = self.defaultConfig
        self.config.update(updateConfig)
        self.times = self.config["次数"]
        self.islandsPriorityTemplateList = [
            self.config[islands] for islands in self.config["岛屿选择优先列表"]
        ]
        self.buffPriorityTemplateList = [
            OcrTemplate(text=buff, isGary=True, useCache=True)
            for buff in self.config["BUFF选择优先列表"]
        ]
        self.readyTask = ReadyTask(device)
        self.settleSixStreet = SettleTask(device, settleTemplate=self.config["结算铃铛"])
        self.settleBoss = SettleTask(device, settleTemplate=self.config["结算击败"])
        self.islandsTimes = 0  # 进入岛屿次数

    def run(self):
        # 判断任务次数是否已经符合条件
        if self.runTimes >= self.times:
            self.done = True
            return
        # 开启阶段
        self.__enterSixStreet()
        # 挑战
        self.device.findAndClick(self.config["通用挑战"])
        # 准备阶段
        self.readyTask.run()
        # 结算阶段
        self.__settle()
        # 选择buff阶段
        self.__selectBuff()
        # 选择岛屿
        self.__selectIslands()
        # 各种岛屿处理
        self.__islandsFunc()

    def __islandsFunc(self):
        if self.device.find(self.config["岛屿页面"]):
            # 剩余1轮时，点击备战识别柔风等级是否开个宁息
            # 神秘岛屿
            if self.device.find(self.config["神秘之屿"]):
                # 转换或者柔风5级
                # 左上角退出
                if self.device.find(self.config["技能转换"]) or self.device.find(
                        self.config["仿造_柔风5级"]
                ):
                    self.device.findAndClick(self.config["退出岛屿"])
                # 仿造
                # 仿造柔风，柔风满级则退出
                if self.device.find(self.config["背包仿造"]):
                    self.device.findAndClick(self.config["仿造"])
                    self.device.rangeRandomClick(self.config["仿造_柔风位置"])
                    self.device.findAndClick(self.config["仿造_确定"])
            # 宁息岛屿 TODO:遇到商店金币不够用，暂时取消掉购买逻辑，直接退出
            if self.device.find(self.config["宁息之屿"]):
                # if self.device.findAndClick(self.Config["通用确定"]):
                #     return
                # # 购买BUFF
                # self.device.find(self.Config["通用确定"])
                # # 如果有柔风就选柔风...等等，没有就选最后一个
                # for template in self.buffPriorityTemplateList[:-1]:
                #     rf_region = self.device.find(template)
                #     if rf_region:
                #         self.device.rangeRandomClick(result=rf_region)
                #         return
                # # 退出
                self.device.findAndClick(self.config["宁息_离开"])
            # 混乱岛屿
            if self.device.find(self.config["混沌之屿"]):
                # 宝箱
                self.device.findAndClick(self.config["混沌_离开"])
                # 精英
                self.device.findAndClick(self.config["精英"])
            # 鏖战之屿
            if self.device.find(self.config["鏖战之屿"]):
                self.device.findAndClick(self.config["普通_鏖战之屿"])
            # 星之岛屿
            if self.device.find(self.config["星之屿"]):
                self.device.findAndClick(self.config["普通_星之屿"])

    def __selectBuff(self):
        if self.device.find(self.config["BUFF选择页面"]):
            time.sleep(self.config["BUFF选择延迟"])
            self.device.find(self.config["通用确定"])
            # 如果有柔风就选柔风...等等，没有就选最后一个
            for template in self.buffPriorityTemplateList[:-1]:
                rf_region = self.device.find(template)
                if rf_region:
                    self.config["选择"].region = rf_region[0:3] + [SCREEN_HEIGHT]
                    self.device.findAndClick(self.config["选择"])
                    return
            if (
                    self.device.find(self.config["铃铛为0"])
                    or (self.islandsTimes < self.config["进入岛屿多少次后刷新技能"])
                    or not self.device.findAndClick(self.config["BUFF刷新"], isColor=True)
            ):
                rf_region = self.device.find(self.buffPriorityTemplateList[-1])
                if rf_region:
                    self.config["选择"].region = rf_region[0:3] + [SCREEN_HEIGHT]
                    self.device.findAndClick(self.config["选择"])

    def __selectIslands(self):
        if self.device.find(self.config["唤息"]):
            time.sleep(self.config["岛屿动画延迟"])
            # 选择岛屿阶段
            for template in self.islandsPriorityTemplateList:
                if self.device.findAndClick(template):
                    self.islandsTimes += 1  # 进入岛屿次数自增
                    return

    def __settle(self):
        # 结算阶段
        self.settleSixStreet.run()
        if self.settleBoss.run():
            self.runTimes += 1
            self.islandsTimes = 0  # 重置进入岛屿次数
            loguru.logger.info(self)

    def __enterSixStreet(self):
        if self.device.find(self.config["攻略"]):
            self.device.findAndClick(self.config["开启"])
            self.device.findAndClick(self.config["开启_2"])
            self.device.findAndClick(self.config["确定"])

    def __str__(self) -> str:
        return "六道任务——萤草速刷<{}/{}>".format(self.runTimes, self.times)
