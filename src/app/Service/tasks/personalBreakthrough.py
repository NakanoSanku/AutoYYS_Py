#  个人突破逻辑实现
import time

from pygamescript import GameScript, ImageTemplate
from loguru import logger

from src.config import IMAGES_DIR
from .ready import ReadyTask
from .settle import SETTLE_FAIL, SETTLE_REWARD, SETTLE_WIN, SettleTask


class PersonalBreakthrough:
    defaultConfig = {
        "突破图标": ImageTemplate(
            templatePath=IMAGES_DIR + "/个人突破/结界突破.png", describe="突破图标",
            region=[200, 600, 400, 720]
        ),
        "刷新": ImageTemplate(
            templatePath=IMAGES_DIR + "/个人突破/刷新.png", describe="刷新按钮",
            region=[900, 550, 1200, 650]
        ),
        "刷新确认": ImageTemplate(
            templatePath=IMAGES_DIR + "/个人突破/刷新确认.png", describe="刷新确认按钮",
            region=[600, 300, 900, 500]
        ),
        "进攻": ImageTemplate(
            templatePath=IMAGES_DIR + "/个人突破/进攻.png", describe="进攻按钮",
            region=[100, 300, 1200, 700]
        ),
        "突破胜利标识": ImageTemplate(
            templatePath=IMAGES_DIR + "/个人突破/突破胜利标识.png", describe="突破胜利标识", threshold=0.8,
            region=[140, 140, 1200, 550]
        ),
        "防守记录": ImageTemplate(
            templatePath=IMAGES_DIR + "/个人突破/防守记录.png", describe="防守记录",
            region=[100, 600, 200, 720]
        ),
        "关闭突破": ImageTemplate(
            templatePath=IMAGES_DIR + "/个人突破/关闭突破.png", describe="关闭突破",
            region=[1100, 50, 1250, 200]
        ),
        "是否保级": True,
        "失败次数阈值": 4,
        "退出阈值": 8,
        "突破成功动画补偿时间": 0.5,
        "点击进攻延迟": 2,
        "个人突破范围矩阵": [[250, 144, 470, 270], [570, 144, 800, 270], [900, 144, 1130, 270],
                             [250, 280, 470, 405], [570, 280, 800, 405], [893, 280, 1130, 405],
                             [250, 420, 470, 540], [570, 420, 800, 540], [900, 420, 1130, 540]],
    }

    def __init__(self, device: GameScript, updateConfig=None) -> None:
        if updateConfig is None:
            updateConfig = {}
        self.device = device
        self.done = False
        self.complete = False
        self.winTimes = 0  # 初始化突破成功次数
        self.failTimes = 0  # 初始化突破失败次数
        self.config = self.defaultConfig
        self.config.update(updateConfig)
        # 准备阶段任务初始化
        self.isExit = False  # 绑定是否退出战斗的变量
        self.readyTask = ReadyTask(self.device, self.isExit)
        # 结算阶段任务初始化
        self.settleTaskReward = SettleTask(self.device, SETTLE_REWARD)
        self.settleTaskWin = SettleTask(self.device, SETTLE_WIN, isColor=True)
        self.settleTaskFail = SettleTask(self.device, SETTLE_FAIL, isColor=True, fightAgain=True)

    def run(self):
        # 7次找图
        # 探索界面阶段
        self.__explorePageStage()
        # 个人突破界面阶段
        self.__personalBreakthroughPageStage()
        # 准备阶段
        self.readyTask.isExit = True if self.winTimes == self.config["退出阈值"] and self.failTimes < self.config[
            "失败次数阈值"] else False
        self.readyTask.run()
        # 结算阶段
        if self.settleTaskFail.run():
            self.failTimes += 1
        self.settleTaskReward.run()
        self.settleTaskWin.run()

    def __explorePageStage(self):
        result = self.device.find(self.config["突破图标"])
        if result:
            if self.complete:
                self.done = True
            else:
                self.device.rangeRandomClick(result)

    def __personalBreakthroughPageStage(self):
        if self.complete:
            self.device.findAndClick(self.config["关闭突破"])
        else:
            if self.device.find(self.config["防守记录"], isColor=True):
                time.sleep(self.config["突破成功动画补偿时间"])
                for index, region in enumerate(self.config["个人突破范围矩阵"]):
                    self.config["突破胜利标识"].region = region
                    if not self.device.find(self.config["突破胜利标识"]):
                        self.device.rangeRandomClick(region)
                        self.winTimes = index
                        break
                if self.winTimes == 0:
                    self.failTimes = 0
            if self.device.findAndClick(self.config["进攻"]):
                time.sleep(self.config["点击进攻延迟"])
                if self.device.find(self.config["进攻"]):
                    self.complete = True

    def __str__(self) -> str:
        return "个人突破\n胜利次数:{}\n失败次数:{}".format(self.winTimes, self.failTimes)
