from src.tasks.base.manual2autoFight.task import manual2autoFight
from src.tasks.base.ready.task import ready
from src.tasks.base.settle.task import *
from src.tasks.fightSkill.assets import *


def fightSkill(device: GameScript):
    while True:
        device.findAndClick(FIGHT_SKILL_FIGHT)
        # 准备
        ready(device)
        # 上阵
        device.findAndClick(FIGHT_SKILL_GO_INTO_BATTLE)
        # 自动战斗
        manual2autoFight(device)
        # 结算
        settleWin(device)
        settleFail(device)
        settleReward(device)
        # 休息
        time.sleep(0.8)
