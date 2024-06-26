import random
import time

from pygamescript import Template, GameScript, ImageTemplate, ImageColorTemplate

from src.config import IMAGES_DIR

SETTLE_VIEW = ImageTemplate(
    template_path=IMAGES_DIR + "/结算/结算视图.png",
    describe="结算视图",
    region=[0, 0, 150, 720],
)
SETTLE_WIN = ImageColorTemplate(
    template_path=IMAGES_DIR + "/结算/结算胜利.png",
    describe="结算胜利",
    threshold=0.8,
    region=[349, 74, 642, 321],
)
SETTLE_REWARD = ImageTemplate(
    template_path=IMAGES_DIR + "/结算/结算奖励.png",
    describe="结算奖励",
    threshold=0.8,
    region=[454, 372, 817, 653]
)
SETTLE_FAIL = ImageColorTemplate(
    template_path=IMAGES_DIR + "/结算/结算失败.png",
    describe="结算失败",
    region=[349, 74, 642, 321],
)

FIGHT_AGAIN = ImageTemplate(
    template_path=IMAGES_DIR + "/结算/再次挑战.png",
    describe="再战",
    threshold=0.8,
    region=[791, 439, 951, 592],
)

CONFIRM = ImageTemplate(
    template_path=IMAGES_DIR + "/结算/再次挑战确认.png",
    describe="再战确定",
    threshold=0.8,
    region=[653, 387, 868, 482],
)
DEFAULT_SETTLE_RESULT_LIST = [[10, 100, 120, 550], [1150, 50, 1280, 720]]

SETTLE_SLEEP_TIME = 0


class SettleTask:
    SETTLE_APPEAR = 1
    SETTLE_DISAPPEAR = 0

    def __init__(
            self,
            device: GameScript,
            settleTemplate: Template,
            settleResultList=None,
            fightAgain=False,
    ) -> None:
        """结算任务

        Args:
            device (GameScript): GameScript实例化
            settleResultList (list, optional): 结算点位列表 默认值为DEFAULT_SETTLE_RESULT_LIST
            isColor (bool, optional): 是否判断结算标志的颜色. Defaults to False.
            colorThreshold (int, optional): 结算标志的颜色的匹配阈值. Defaults to 4.
            fightAgain (bool, optional): 是否点击再次挑战,仅在结算失败时有效. Defaults to False.

        Raises:
            Exception: 当settleType不在SettleTask.getSettleTypeList()中时抛出异常
        """
        self.device = device
        self.settleTemplate = settleTemplate
        self.settleResultList = (
            DEFAULT_SETTLE_RESULT_LIST if not settleResultList else settleResultList
        )
        self.fightAgain = fightAgain if settleTemplate == SETTLE_FAIL else False
        self.settleMark = SettleTask.SETTLE_DISAPPEAR

    def run(self):
        if self.__settle(self.settleTemplate):
            # 找到结算标志 更新结算标志
            self.settleMark = SettleTask.SETTLE_APPEAR
            if self.fightAgain:
                self.device.find_and_click(FIGHT_AGAIN)
        elif self.settleMark == SettleTask.SETTLE_APPEAR:
            # 结算标志消失了，执行其他操作
            return self.__settleOperate()

    def __settleOperate(self):
        if self.fightAgain:
            # 再次挑战逻辑
            if self.device.find_and_click(CONFIRM):
                # 点击完确认返回True并更新标志
                self.settleMark = SettleTask.SETTLE_DISAPPEAR
                return True
        else:
            # 不再次挑战情况下更新标志为消失并返回True
            self.settleMark = SettleTask.SETTLE_DISAPPEAR
            return True

    def __settle(self, template: Template):
        res = self.device.find(template)
        if res and not self.fightAgain:
            # 找到结算标志并且不再次挑战时执行结算操作
            self.device.range_random_click(result=random.choice(self.settleResultList))
            time.sleep(SETTLE_SLEEP_TIME)
        return res

    def __str__(self):
        return "{}结算任务".format(self.settleTemplate)
