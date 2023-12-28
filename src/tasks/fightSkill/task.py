from src.tasks.base.ready.task import ready
from src.tasks.base.settle.task import SettleTask
from src.tasks.base.baseTask import BaseTask
from src.tasks.fightSkill.assets import FIGHT_SKILL_FIGHT, FIGHT_SKILL_GO_INTO_BATTLE, MANUAL
from pygamescript import GameScript


class FightSkillTask(BaseTask):
    def __init__(self, device: GameScript) -> None:
        self.device = device
        self.settleWin = SettleTask(device, SettleTask.SETTLE_WIN_TPYE)
        self.settleFail = SettleTask(device, SettleTask.SETTLE_FAIL_TPYE)
        self.settleReward = SettleTask(device, SettleTask.SETTLE_REWARD_TPYE)

    def run(self):
        # 准备
        ready(self.device)
        self.device.findAndClick(FIGHT_SKILL_FIGHT)
        # 上阵
        self.device.findAndClick(FIGHT_SKILL_GO_INTO_BATTLE)
        self.device.findAndClick(MANUAL)
        self.settleWin.run()
        self.settleFail.run()
        self.settleReward.run()

    def __str__(self) -> str:
        return "FightSkillTask"
