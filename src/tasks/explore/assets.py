from pygamescript import *

from src.config import IMAGES_DIR

CHAPTER_SELECTION = ImageTemplate(templatePath=IMAGES_DIR + "/explore/CHAPTER_SELECTION.png", describe="探索章节选择")
BOSS = ImageTemplate(templatePath=IMAGES_DIR + "/explore/BOSS.png", describe="BOSS")
MONSTER = ImageTemplate(templatePath=IMAGES_DIR + "/explore/MONSTER.png", describe="小怪", threshold=0.75)
CHEST = ImageTemplate(templatePath=IMAGES_DIR + "/explore/CHEST.png", describe="宝箱")
EXPLORE_BUTTON = ImageTemplate(templatePath=IMAGES_DIR + "/explore/EXPLORE_BUTTON.png", describe="探索按钮")
EXPLORE_EXIT_CONFIRM = ImageTemplate(templatePath=IMAGES_DIR + "/explore/EXPLORE_EXIT_CONFIRM.png",
                                     describe="探索退出确认")
SHIKIGAMILU = ImageTemplate(templatePath=IMAGES_DIR + "/explore/SHIKIGAMILU.png", describe="式神录")
EXPLORE_EXIT = ImageTemplate(templatePath=IMAGES_DIR + "/explore/EXPLORE_EXIT.png", describe="探索退出")
PINK_X = ImageTemplate(templatePath=IMAGES_DIR + "/explore/PINK_X.png", describe="粉色x")
