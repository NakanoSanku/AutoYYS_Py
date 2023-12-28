import random
import time

from pygamescript import Template, GameScript

from src.tasks.base.settle.assets import *
from src.tasks.base.baseTask import BaseTask


def getSettleTypeList():
    return [SettleTask.SETTLE_WIN_TPYE,
            SettleTask.SETTLE_FAIL_TPYE,
            SettleTask.SETTLE_VIEW_TPYE,
            SettleTask.SETTLE_REWARD_TPYE]


class SettleTask(BaseTask):
    SETTLE_APPEAR = 1
    SETTLE_UNAPPEAR = 0
    SETTLE_WIN_TPYE = SETTLE_WIN
    SETTLE_FAIL_TPYE = SETTLE_FAIL
    SETTLE_VIEW_TPYE = SETTLE_VIEW
    SETTLE_REWARD_TPYE = SETTLE_REWARD

    def __init__(self, device: GameScript, settleType: Template, settleResultList=None, isColor=False, colorThreshold=4,
                 fightAgain=False) -> None:
        """结算任务

        Args:
            device (GameScript): GameScript实例化
            settleType (SETTLE_TYPE_LIST): SETTLE_TYPE_LIST中的元素 通过getSettleTypeList()获取
            settleResultList (list, optional): 结算点位列表 默认值为DEFAULT_SETTLE_RESULT_LIST 可以是[x_min,y_min,x_max,y_max]的二维列表,也可以是(x,y)的坐标点
            isColor (bool, optional): 是否判断结算标志的颜色. Defaults to False.
            colorThreshold (int, optional): 结算标志的颜色的匹配阈值. Defaults to 4.
            fightAgain (bool, optional): 是否点击再次挑战,仅在结算失败时有效. Defaults to False.

        Raises:
            Exception: 当settleType不在SettleTask.getSettleTypeList()中时抛出异常
        """
        self.device = device
        self.settleType = settleType
        self.settleResultList = DEFAULT_SETTLE_RESULT_LIST if not settleResultList else settleResultList
        self.isColor = isColor
        self.colorThreshold = colorThreshold
        self.fightAgain = fightAgain if settleType == SETTLE_FAIL else False
        self.settleMark = SettleTask.SETTLE_UNAPPEAR
        if settleType not in getSettleTypeList():
            raise Exception("settleType is not in SettleTask.getSettleTypeList()")

    def run(self):
        if self.__settle(self.settleType):
            # 找到结算标志 更新结算标志
            self.settleMark = SettleTask.SETTLE_APPEAR
            if self.fightAgain:
                self.device.findAndClick(FIGHT_AGAIN)
        elif self.settleMark == SettleTask.SETTLE_APPEAR:
            # 结算标志消失了，执行其他操作
            return self.__settleOperate()

    def __settleOperate(self):
        if self.fightAgain:
            # 再次挑战逻辑
            if self.device.findAndClick(CONFIRM):
                # 点击完确认返回True并更新标志
                self.settleMark = SettleTask.SETTLE_UNAPPEAR
                return True
        else:
            # 不再次挑战情况下更新标志为消失并返回True
            self.settleMark = SettleTask.SETTLE_UNAPPEAR
            return True

    def __settle(self, template: Template):
        res = self.device.find(template, isColor=self.isColor, colorThreshold=self.colorThreshold)
        if res and not self.fightAgain:
            # 找到结算标志并且不再次挑战时执行结算操作
            self.device.rangeRandomClick(result=random.choice(self.settleResultList))
            time.sleep(SETTLE_SLEEP_TIME)
        return res

    def __str__(self):
        return "{}结算任务".format(self.settleType)


def settle(device: GameScript, template: Template, settleResultList=None, isColor=False, colorThreshold=4,
           fightAgain=False):
    settleResultList = DEFAULT_SETTLE_RESULT_LIST if not settleResultList else settleResultList
    res = None
    p = device.find(template, isColor=isColor, colorThreshold=colorThreshold)
    if p:
        res = p
        if fightAgain and template == SETTLE_FAIL:
            while True:
                if device.findAndClick(CONFIRM):
                    break
                device.findAndClick(FIGHT_AGAIN)
        else:
            while device.find(template, isColor=isColor, colorThreshold=colorThreshold):
                device.rangeRandomClick(result=random.choice(settleResultList))
                time.sleep(SETTLE_SLEEP_TIME)
    return res


def settleWin(device: GameScript, settleResultList=None):
    return settle(device, SETTLE_WIN, settleResultList, isColor=True, colorThreshold=15)


def settleView(device: GameScript, settleResultList=None):
    return settle(device, SETTLE_VIEW, settleResultList)


def settleFail(device: GameScript, settleResultList=None, fightAgain=False):
    return settle(device, SETTLE_FAIL, settleResultList, isColor=True, colorThreshold=15, fightAgain=fightAgain)


def settleReward(device: GameScript, settleResultList=None):
    return settle(device, SETTLE_REWARD, settleResultList)


if __name__ == '__main__':
    from pygamescript import GameScript
    from minidevice import DroidCast, ADBtouch
    from adbutils import adb

    serial = adb.device_list()[0].serial
    ld = GameScript(serial, DroidCast, ADBtouch)
    settt = SettleTask(ld, SettleTask.SETTLE_FAIL_TPYE, fightAgain=True, isColor=True)


    def func():
        # device.findAndClick(CONFIRM)
        while 1:
            settt.run()
            time.sleep(1)


    func()
