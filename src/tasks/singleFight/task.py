import time

import loguru
from pygamescript import GameScript

from src.tasks.singleFight.assets import SINGLE_FIGHT
from src.tasks.base.settle.task import settleWin, settleFail, settleReward


def singleFight(device: GameScript, times: int):
    i = 0
    while i < times:
        device.findAndClick(SINGLE_FIGHT)
        settleFail(device)
        settleWin(device)
        if settleReward(device):
            i += 1
            loguru.Logger.info(f"第{i}次结算成功")
