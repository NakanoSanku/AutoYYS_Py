import loguru
from pygamescript import GameScript

from src.tasks.base.settle.task import settleFail, settleView
from src.tasks.teamFight.assets import TEAM_FIGHT, THREE_PLAYER


def teamFight(device: GameScript, times: int, isLeader=False, threePlayer=False):
    i = 0
    while i < times:
        if isLeader:
            if not (threePlayer and device.find(THREE_PLAYER)):
                device.findAndClick(TEAM_FIGHT, isColor=True)
        if not settleFail(device):
            if settleView(device):
                i += 1
                loguru.Logger.info(f"第{i}次结算成功")
