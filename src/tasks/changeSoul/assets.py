from pygamescript import *

from src.config import IMAGES_DIR

GROUP_REGION_LIST = [[1084, 87, 1247, 154], [1084, 154, 1249, 225], [1085, 226, 1248, 293],
                     [1086, 294, 1249, 364], [1086, 364, 1247, 433], [1085, 434, 1247, 504],
                     [1084, 505, 1247, 573]]

TEAM_REGION_LIST = [[965, 140, 1018, 190], [964, 288, 1020, 342], [962, 441, 1018, 493]]
PRESET_2 = ImageTemplate(templatePath=IMAGES_DIR + "/changeSoul/预设2.png")
PRESET = ImageTemplate(templatePath=IMAGES_DIR + "/changeSoul/预设1.png")
SHIIKSA = ImageTemplate(templatePath=IMAGES_DIR + "/changeSoul/式神录.png")
APPLY_PRESET = ImageTemplate(templatePath=IMAGES_DIR + "/changeSoul/应用预设.png", )
CONFIRM = ImageTemplate(templatePath=IMAGES_DIR + "/changeSoul/确认.png")
EXIT = ImageTemplate(templatePath=IMAGES_DIR + "/changeSoul/退出.png")
COLORS_TEMPLATE = ColorsTemplate("#f8d89f",
                                 [[40, -2, "#f8d9a0"], [78, -1, "#f8d699"], [124, 13, "#f3c26e"],
                                  [132, 36, "#f5c36e"], [32, 37, "#f8d598"], [15, 18, "#f8d89f"]],
                                 threshold=4)
