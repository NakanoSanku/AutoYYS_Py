from pygamescript import *

from src.config import IMAGES_DIR

ALREADY_DRIVE = ImageTemplate(templatePath=IMAGES_DIR + "/soloEnchantment/ALREADY_DRIVE.png", describe="已突破图标",
                              threshold=0.75)
SHIKIGAMILU = ImageTemplate(templatePath=IMAGES_DIR + "/soloEnchantment/SHIKIGAMILU.png", describe="式神录")
SOLO_DRIVE_REGION_LIST = [[250, 144, 470, 270], [570, 144, 800, 270], [900, 144, 1130, 270],
                          [250, 280, 470, 405], [570, 280, 800, 405], [893, 280, 1130, 405],
                          [250, 420, 470, 540], [570, 420, 800, 540], [900, 420, 1130, 540]]
REFRESH = ImageTemplate(templatePath=IMAGES_DIR + "/soloEnchantment/REFRESH.png", describe="刷新图标")
REFRESH_CONFIRM = ImageTemplate(templatePath=IMAGES_DIR + "/soloEnchantment/REFRESH_CONFIRM.png", describe="确认刷新图标")