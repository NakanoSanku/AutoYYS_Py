import random
import time

from pygamescript import GameScript, algo

from src.tasks.base.baseTask import BaseTask
from src.tasks.base.settle.task import SettleTask
from src.tasks.explore.assets import *
from loguru import logger


class ExploreTask(BaseTask):
    # 未知页面
    UNDEFINED_PAGE = -1
    # 探索页面
    EXPLORE_PAGE = 0
    # 章节选择页面
    CHAPTER_PAGE = 1
    # 找怪页面
    FIND_MONSTER_PAGE = 2
    # boss打完了
    BOSS_FUCKED = 0
    # boss没打完
    BOSS_NOT_FUCKED = 1

    def __init__(self, device: GameScript, times: int):
        self.device = device
        self.times = times
        self.runTime = 0
        self.smlMoveTimes = 0
        self.page = ExploreTask.UNDEFINED_PAGE
        self.bossMark = ExploreTask.BOSS_NOT_FUCKED
        self.done = False
        self.settle = SettleTask(self.device, SettleTask.SETTLE_VIEW_TPYE)

    def __selectPage(self):
        """判断当前所处界面"""
        self.page = ExploreTask.UNDEFINED_PAGE
        self.page = ExploreTask.EXPLORE_PAGE if self.device.find(EXPLORE_PAGE) else self.page
        self.page = ExploreTask.CHAPTER_PAGE if self.device.find(CHAPTER_PAGE) else self.page
        self.page = ExploreTask.FIND_MONSTER_PAGE if self.device.find(FIND_MONSTER_PAGE) else self.page

    def run(self):
        # 任务已完成就不执行后续代码
        if self.done:
            return
        # 选择页面
        self.__selectPage()
        if self.settle.run():
            self.runTime += 1
            logger.info(f"第{self.runTime}次结算")
        # 探索页面
        if self.page == ExploreTask.EXPLORE_PAGE:
            if self.runTime == self.times:
                self.done = True
                return
            # 探索章节选择并检测宝箱
            self.device.findAndClick(CHEST)
            self.device.findAndClick(CHAPTER_SELECTION)

        # 章节选择页面
        if self.page == ExploreTask.CHAPTER_PAGE:
            if self.runTime == self.times:
                self.device.findAndClick(PINK_X)
            else:
                self.device.findAndClick(EXPLORE_BUTTON)
            self.bossMark = ExploreTask.BOSS_NOT_FUCKED
        # 找怪页面
        if self.page == ExploreTask.FIND_MONSTER_PAGE:
            # 检查boss是否打完或者探索次数已完成，是则退出探索
            self.__exitExplore()
            if self.runTime < self.times:
                # 找怪打
                self.__findMonster()

    def __exitExplore(self):
        if (self.bossMark == ExploreTask.BOSS_FUCKED) or (self.runTime == self.times):
            if self.device.findAndClick(EXPLORE_EXIT_CONFIRM):
                time.sleep(EXIT_EXPLORE_DELAY_TIME)
                return
            self.device.findAndClick(EXPLORE_EXIT)

    def __findMonster(self):
        if self.bossMark == ExploreTask.BOSS_NOT_FUCKED:
            # 检测boss
            if self.device.findAndClick(BOSS):
                self.smlMoveTimes = 0
                self.bossMark = ExploreTask.BOSS_FUCKED
                logger.info("探索完成")
                time.sleep(1)
            # 检测小怪
            elif self.device.findAndClick(MONSTER):
                self.smlMoveTimes = 0
                logger.info("小怪出现")
                time.sleep(1)
            # 滑动
            else:
                self.__swipe()

    def __swipe(self):
        if self.smlMoveTimes == MAX_SWIPE_TIMES:
            self.bossMark = ExploreTask.BOSS_FUCKED
            self.smlMoveTimes = 0
        else:
            startX, startY = algo.RandomPointGenerate.normalDistribution(SWIPE_START_REGION)
            endX, endY = algo.RandomPointGenerate.normalDistribution(SWIPE_END_REGION)
            swipeDuration = random.randint(SWIPE_DURATION_MIN, SWIPE_DURATION_MAX)
            self.device.curveSwipe(startX, startY, endX, endY, swipeDuration)
            self.smlMoveTimes += 1
            logger.info("滑动")

    def __str__(self):
        return "探索任务--已执行次数({}/{})".format(self.runTime, self.times)
