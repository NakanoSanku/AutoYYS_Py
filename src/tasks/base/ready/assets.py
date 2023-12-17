from pygamescript import *

from src.config import IMAGES_DIR

READY = ImageTemplate(templatePath=IMAGES_DIR + "ready/READY.png", describe="准备按钮")
EXIT = ImageTemplate(templatePath=IMAGES_DIR + "ready/EXIT.png", describe="退出战斗")
EXIT_CONFIRM = ImageTemplate(templatePath=IMAGES_DIR + "ready/EXIT_CONFIRM.png", describe="退出确认")
