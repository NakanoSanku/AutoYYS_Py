import time

import loguru
from pygamescript import GameScript

from src.tasks.base.baseTask import BaseTask
from src.tasks.base.ready.task import ReadyTask
from src.tasks.base.settle.task import SettleTask
from src.tasks.soloEnchantment.assets import *


class SoloEnchantmentTask(BaseTask):
    UNDEFINED_PAGE = -1
    EXPLORE_PAGE = 0
    SOLO_ENCHANTMENT_PAGE = 1

    def __init__(self, device: GameScript, is_ensure_level=True) -> None:
        self.done = False
        self.is_ensure_level = is_ensure_level
        self.device = device
        self.number_of_failures = 0
        self.number_of_victory = 0
        self.isExit = False
        self.readyTask = ReadyTask(self.device, isExit=self.isExit)
        self.settleReward = SettleTask(self.device, SettleTask.SETTLE_REWARD_TPYE)
        self.settleFail = SettleTask(self.device, SettleTask.SETTLE_FAIL_TPYE, fightAgain=self.isExit, isColor=True)
        self.settleWin = SettleTask(self.device, SettleTask.SETTLE_WIN_TPYE, isColor=True)
        self.page = SoloEnchantmentTask.UNDEFINED_PAGE
        self.ticket = 1

    def __enterEnchantment(self):
        self.device.findAndClick(SOLO_ENCHANTMENT)
        self.device.findAndClick(ENCHANTMENT)

    def __selectPage(self):
        self.page = SoloEnchantmentTask.UNDEFINED_PAGE
        if self.device.find(SOLO_ENCHANTMENT_PAGE, isColor=True):
            self.page = SoloEnchantmentTask.SOLO_ENCHANTMENT_PAGE
        elif self.device.find(EXPLORE_PAGE):
            self.page = SoloEnchantmentTask.EXPLORE_PAGE

    def __reset(self):
        # 重置胜利和失败次数
        self.number_of_victory = 0
        self.number_of_failures = 0
        loguru.logger.info("重置胜利和失败次数")

    def __refresh(self):
        # 刷新逻辑
        if (self.number_of_victory < 3 and self.number_of_failures > 0) or self.number_of_failures > 4:
            self.device.findAndClick(REFRESH)
            self.device.findAndClick(REFRESH_CONFIRM)

    def __enchantmentFight(self):
        if self.device.findAndClick(ATTACK):
            time.sleep(1)
            if self.device.find(ATTACK):
                self.ticket = 0

    def __exit(self):
        self.device.findAndClick(PINK_X)

    def run(self):
        if self.done:
            return
        self.__selectPage()

        # 保级退出逻辑
        if self.is_ensure_level:
            self.isExit = True if self.number_of_victory == 8 and self.number_of_failures < 4 else False
            self.settleFail.fightAgain = self.isExit
            self.readyTask.isExit = self.isExit

        if self.page == SoloEnchantmentTask.EXPLORE_PAGE:
            # 进入突破界面
            if self.ticket == 0:
                self.done = True
                return
            self.__enterEnchantment()

        if self.page == SoloEnchantmentTask.SOLO_ENCHANTMENT_PAGE:
            # 选择攻击对象
            number_of_victory = 0
            for i, index in enumerate(SOLO_DRIVE_REGION_LIST):
                ALREADY_DRIVE.region = index
                if self.device.find(ALREADY_DRIVE):
                    number_of_victory = number_of_victory + 1
                else:
                    self.device.rangeRandomClick(result=index)
                    time.sleep(0.5)
                    break
            loguru.logger.info(f"胜利次数: {number_of_victory}")
            self.number_of_victory = number_of_victory
            if number_of_victory == 0:
                self.__reset()

        if self.page == SoloEnchantmentTask.UNDEFINED_PAGE:
            # 准备逻辑
            self.readyTask.run()
            # 结算逻辑
            self.settleWin.run()

            if self.settleFail.run():
                self.number_of_failures += 1
                loguru.logger.info(f"失败次数: {self.number_of_failures}")

            self.settleReward.run()
            # 进攻
            self.__enchantmentFight()

            # 刷新
            self.__refresh()

            if self.ticket == 0:
                self.__exit()
                return

    def __str__(self):
        return "突破任务"
