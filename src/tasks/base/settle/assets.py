from pygamescript import *

from src.config import IMAGES_DIR

SETTLE_VIEW = ImageTemplate(templatePath=IMAGES_DIR + "/settle/SETTLE_VIEW.png", describe="结算视图")
SETTLE_WIN = ImageTemplate(templatePath=IMAGES_DIR + "/settle/SETTLE_WIN.png", describe="结算胜利", threshold=0.8)
SETTLE_REWARD = ImageTemplate(templatePath=IMAGES_DIR + "/settle/SETTLE_REWARD.png", describe="结算奖励", threshold=0.8)
SETTLE_FAIL = ImageTemplate(templatePath=IMAGES_DIR + "/settle/SETTLE_FAIL.png", describe="结算失败")
