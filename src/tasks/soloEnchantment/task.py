import time

import loguru

from src.tasks.base.enchantmentFight.task import enchantmentFight
from src.tasks.base.enterEnchantment.task import enterEnchantment
from src.tasks.base.ready.task import ready
from src.tasks.base.settle.task import settleReward, settleFail, settleWin
from assets.images.soloEnchantment.assets import *

from assets.images.soloEnchantment.assets import REFRESH, REFRESH_CONFIRM


def refreshEnchantment(device: GameScript):
    while True:
        if device.findAndClick(REFRESH):
            loguru.logger.info("刷新")
        if device.findAndClick(REFRESH_CONFIRM):
            time.sleep(2)
            if not device.find(REFRESH_CONFIRM):
                time.sleep(1)
                break


def soloEnchantment(_device: GameScript, is_ensure_level=True):
    number_of_failures = 0
    number_of_victory = 0
    isExit = False

    # 进入突破界面
    enterEnchantment(_device, '个突')

    while True:
        # 重置胜利和失败次数
        if number_of_victory == 9:
            number_of_victory = 0
            number_of_failures = 0
            loguru.logger.info("重置胜利和失败次数")

        # 刷新逻辑
        if (number_of_victory < 3 and number_of_failures > 0) or number_of_failures > 4:
            refreshEnchantment(_device)
            number_of_victory = 0
            number_of_failures = 0
            loguru.logger.info("重置胜利和失败次数")

        # 进攻
        if enchantmentFight(_device):
            break

        # 保级退出逻辑
        if is_ensure_level:
            isExit = True if number_of_victory == 8 and number_of_failures < 4 else False

        # 准备逻辑
        ready(_device, isExit)

        # 结算逻辑
        if settleWin(_device):
            number_of_victory += 1
        if settleFail(_device):
            number_of_failures += 1
            loguru.logger.info(f"失败次数: {number_of_failures}")
        if not settleReward(_device):
            # 选择攻击对象
            if _device.find(SHIKIGAMILU):
                time.sleep(1)
                for index, i in zip(SOLO_DRIVE_REGION_LIST, range(len(SOLO_DRIVE_REGION_LIST))):
                    ALREADY_DRIVE.region = index
                    if _device.find(ALREADY_DRIVE):
                        number_of_victory = i + 1
                        loguru.logger.info(f"胜利次数: {number_of_victory}")
                    else:
                        _device.rangeRandomClick(result=index)
                        time.sleep(0.5)
                        break

        # 休息
        time.sleep(0.5)
