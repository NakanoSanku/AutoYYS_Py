from pygamescript import ImageTemplate, ColorsTemplate

from src.config import IMAGES_DIR

CHAPTER_SELECTION = ImageTemplate(templatePath=IMAGES_DIR + "/explore/CHAPTER_SELECTION.png", describe="探索章节选择")
BOSS = ImageTemplate(templatePath=IMAGES_DIR + "/explore/BOSS.png", describe="BOSS")
MONSTER = ImageTemplate(templatePath=IMAGES_DIR + "/explore/MONSTER.png", describe="小怪", threshold=0.75)
CHEST = ImageTemplate(templatePath=IMAGES_DIR + "/explore/CHEST.png", describe="宝箱")
EXPLORE_BUTTON = ImageTemplate(templatePath=IMAGES_DIR + "/explore/EXPLORE_BUTTON.png", describe="探索按钮")
EXPLORE_EXIT_CONFIRM = ImageTemplate(templatePath=IMAGES_DIR + "/explore/EXPLORE_EXIT_CONFIRM.png",
                                     describe="探索退出确认")
SHIKIGAMILU = ImageTemplate(templatePath=IMAGES_DIR + "/explore/SHIKIGAMILU.png", describe="式神录",
                            region=[758, 615, 870, 719])
EXPLORE_EXIT = ImageTemplate(templatePath=IMAGES_DIR + "/explore/EXPLORE_EXIT.png", describe="探索退出")
PINK_X = ImageTemplate(templatePath=IMAGES_DIR + "/explore/PINK_X.png", describe="粉色x")

MAX_SWIPE_TIMES = 5
SWIPE_START_REGION = [1000, 120, 1100, 120]
SWIPE_END_REGION = [500, 90, 600, 120]
SWIPE_DURATION_MIN = 350
SWIPE_DURATION_MAX = 400

EXPLORE_PAGE = ImageTemplate(templatePath=IMAGES_DIR+"/explore/探索界面.png", describe="探索页面")

CHAPTER_PAGE = PINK_X

FIND_MONSTER_PAGE = SHIKIGAMILU

EXIT_EXPLORE_DELAY_TIME = 1

if __name__ == '__main__':
    from pygamescript import GameScript
    from minidevice import DroidCast, ADBtouch
    from adbutils import adb
    import cProfile

    serial = adb.device_list()[0].serial
    device = GameScript(serial, DroidCast, ADBtouch)


    def func():
        device.find(EXPLORE_PAGE)


    func()
    # cProfile.run("func()")
