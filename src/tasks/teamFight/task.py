import loguru
from pygamescript import GameScript

from src.tasks.teamFight.assets import TEAM_FIGHT, THREE_PLAYER
from src.tasks.base.settle.task import SettleTask
from src.tasks.base.baseTask import BaseTask


class TeamFight(BaseTask):
    def __init__(self, device: GameScript, times: int, isLeader=False, isThreePlayer=False) -> None:
        self.device = device
        self.times = times
        self.isLeader = isLeader
        self.isThreePlayer = isThreePlayer
        self.runTime = 0
        self.settleView = SettleTask(self.device, SettleTask.SETTLE_VIEW_TPYE)

    def run(self):
        if self.isLeader:
            if not (self.isThreePlayer and self.device.find(THREE_PLAYER)):
                self.device.findAndClick(TEAM_FIGHT, isColor=True)
        if self.settleView.run():
            self.runTime += 1
            loguru.logger.info(f"第{self.runTime}次结算成功")

    def __str__(self):
        return "战斗，执行次数:({}/{})".format(self.runTime, self.times)
