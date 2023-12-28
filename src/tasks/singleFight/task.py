import loguru
from pygamescript import GameScript

from src.tasks.singleFight.assets import SINGLE_FIGHT
from src.tasks.base.settle.task import SettleTask
from src.tasks.base.baseTask import BaseTask


class SingleFight(BaseTask):
    def __init__(self, device: GameScript, times: int) -> None:
        self.device = device
        self.times = times
        self.runTime = 0
        self.settleWin = SettleTask(device, SettleTask.SETTLE_WIN_TPYE)
        self.settleFail = SettleTask(device, SettleTask.SETTLE_FAIL_TPYE)
        self.settleReward = SettleTask(device, SettleTask.SETTLE_REWARD_TPYE)

    def run(self):
        self.device.findAndClick(SINGLE_FIGHT)
        self.settleWin.run()
        self.settleFail.run()
        if self.settleReward.run():
            self.runTime += 1
            loguru.logger.info(f"第{self.runTime}次结算成功")

    def __str__(self):
        return "单人战斗，执行次数:({}/{})".format(self.runTime, self.times)
