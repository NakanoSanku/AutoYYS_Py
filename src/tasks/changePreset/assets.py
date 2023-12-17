from pygamescript import *

from src.config import IMAGES_DIR

SINGLE_FIGHT = ImageTemplate(templatePath=IMAGES_DIR + "/singleFight/SINGLE_FIGHT.png", describe="描述")
READY = ImageTemplate(templatePath=IMAGES_DIR + "/changePreset/准备.png")
PRESET_SWIPE = ImageTemplate(templatePath=IMAGES_DIR + "/changePreset/预设滑动.png")
COLORS_TEMPLATE = ColorsTemplate("#f8d99f",
                                 [[34, 0, "#f8d89e"], [60, -1, "#f8d597"], [89, 6, "#f4c26e"],
                                  [92, 24, "#f8c877"], [96, 30, "#f4c26d"], [67, 31, "#f9d596"],
                                  [9, 29, "#f8d699"]])
CONFIRM = ImageTemplate(templatePath=IMAGES_DIR + "/changePreset/确认.png")
GROUP_REGION_LIST = [[32, 238, 168, 299], [30, 299, 167, 361],
                     [32, 365, 167, 422], [33, 426, 167, 487],
                     [31, 489, 168, 551], [32, 552, 167, 613], [31, 616, 166, 679]]
TEAM_REGEION_LIST = [[195, 236, 664, 348], [195, 352, 663, 470], [194, 476, 665, 589]]