import time
import random
import numpy as np

from pygamescript import GameScript, algo
from src.tasks.base.settle.task import settleView
from src.tasks.explore.assets import *
from loguru import logger


def exitExplore(device: GameScript):
    while True:
        if device.findAndClick(EXPLORE_EXIT):
            time.sleep(1.5)
            if device.findAndClick(EXPLORE_EXIT_CONFIRM):
                time.sleep(1)
            return
        time.sleep(0.8)


def exitPinkX(device: GameScript):
    while True:
        if device.findAndClick(PINK_X):
            time.sleep(3)
            if not device.find(PINK_X):
                return
        time.sleep(0.5)


def explore(device: GameScript, times: int):
    mark = 0
    i = 0
    smlMoveTimes = 0
    while i < times:
        # 探索章节选择并检测宝箱
        if device.find(CHAPTER_SELECTION) and not device.findAndClick(CHEST) and device.findAndClick(CHAPTER_SELECTION):
            time.sleep(0.5)
            logger.info("选择章节")

        # 探索按钮检测
        if device.findAndClick(EXPLORE_BUTTON):
            time.sleep(0.5)
            logger.info("进入探索")
            mark = 0

        # 检测式神录
        if device.find(SHIKIGAMILU):
            # 检查boss是否打完，是则退出探索
            if mark == 1:
                exitExplore(device)
            # 找怪打
            if mark == 0:
                # 检测boss
                if device.findAndClick(BOSS):
                    smlMoveTimes = 0
                    time.sleep(1)
                    if not device.find(BOSS):
                        logger.info("探索完成")
                        mark = 1
                # 检测小怪
                elif device.findAndClick(MONSTER):
                    smlMoveTimes = 0
                    time.sleep(1)
                # 滑动
                else:
                    if smlMoveTimes == 5:
                        mark = 1
                        smlMoveTimes = 0
                    else:
                        startX, startY = algo.RandomPointGenerate.normalDistribution([1000, 120, 1100, 120])
                        endX, endY = algo.RandomPointGenerate.normalDistribution([500, 90, 600, 120])

                        device.curveSwipe(startX, startY, endX, endY, random.randint(350, 400))
                        smlMoveTimes += 1
                        logger.info("滑动")

        # 检测结算
        if settleView(device):
            i += 1
            logger.info(f"第{i}次结算")
        # 休息
        time.sleep(0.8)

    # 退出探索
    exitExplore(device)
    # 关闭章节选择
    exitPinkX(device)
