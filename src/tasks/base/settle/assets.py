from pygamescript import ImageTemplate

from src.config import IMAGES_DIR

SETTLE_VIEW = ImageTemplate(templatePath=IMAGES_DIR + "/结算/SETTLE_VIEW.png",
                            describe="结算视图",
                            region=[0, 0, 150, 720])
SETTLE_WIN = ImageTemplate(templatePath=IMAGES_DIR + "/结算/SETTLE_WIN.png",
                           describe="结算胜利",
                           threshold=0.8)
SETTLE_REWARD = ImageTemplate(templatePath=IMAGES_DIR + "/结算/SETTLE_REWARD.png",
                              describe="结算奖励",
                              threshold=0.8)
SETTLE_FAIL = ImageTemplate(templatePath=IMAGES_DIR + "/结算/SETTLE_FAIL.png",
                            describe="结算失败")
FIGHT_AGAIN = ImageTemplate(templatePath=IMAGES_DIR + "/结算/再次挑战.png",
                            describe="再战",
                            threshold=0.8)
CONFIRM = ImageTemplate(templatePath=IMAGES_DIR + "/结算/确定.png",
                        describe="再战确定",
                        threshold=0.8)
DEFAULT_SETTLE_RESULT_LIST = [[10, 100, 120, 550], [1150, 50, 1280, 720]]

SETTLE_SLEEP_TIME = 0.1

SETTLE_TYPE_LIST = [SETTLE_WIN, SETTLE_FAIL,SETTLE_VIEW,SETTLE_REWARD]


if __name__ == '__main__':
    from pygamescript import GameScript
    from minidevice import DroidCast, ADBtouch
    from adbutils import adb
    import cProfile

    serial = adb.device_list()[0].serial
    device = GameScript(serial, DroidCast, ADBtouch)


    def func():
        """主要性能损失还是在将截图上,总消耗时间"""
        print(device.find(CONFIRM))


    cProfile.run('func()')
