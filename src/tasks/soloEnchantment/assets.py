from pygamescript import ImageTemplate

from src.config import IMAGES_DIR

ALREADY_DRIVE = ImageTemplate(templatePath=IMAGES_DIR + "/soloEnchantment/ALREADY_DRIVE.png", describe="已突破图标",
                              threshold=0.75)
SHIKIGAMILU = ImageTemplate(templatePath=IMAGES_DIR + "/soloEnchantment/SHIKIGAMILU.png", describe="式神录")
SOLO_DRIVE_REGION_LIST = [[250, 144, 470, 270], [570, 144, 800, 270], [900, 144, 1130, 270],
                          [250, 280, 470, 405], [570, 280, 800, 405], [893, 280, 1130, 405],
                          [250, 420, 470, 540], [570, 420, 800, 540], [900, 420, 1130, 540]]
REFRESH = ImageTemplate(templatePath=IMAGES_DIR + "/soloEnchantment/REFRESH.png", describe="刷新图标")
REFRESH_CONFIRM = ImageTemplate(templatePath=IMAGES_DIR + "/soloEnchantment/REFRESH_CONFIRM.png",
                                describe="确认刷新图标")
ATTACK = ImageTemplate(templatePath=IMAGES_DIR + "/enchantmentFight/ATTACK.png", describe="突破进攻")
PINK_X = ImageTemplate(templatePath=IMAGES_DIR + "/explore/PINK_X.png", describe="粉色x")
HUT_ENCHANTMENT = ImageTemplate(templatePath=IMAGES_DIR + "/enterEnchantment/HUT_ENCHANTMENT.png",
                                describe="寮突破图标")
SOLO_ENCHANTMENT = ImageTemplate(templatePath=IMAGES_DIR + "/enterEnchantment/SOLO_ENCHANTMENT.png",
                                 describe="个人突破图标")
ENCHANTMENT = ImageTemplate(templatePath=IMAGES_DIR + "/enterEnchantment/ENCHANTMENT.png", describe="突破图标")
EXPLORE_PAGE = ImageTemplate(templatePath=IMAGES_DIR + "/explore/探索界面.png", describe="探索页面")
SOLO_ENCHANTMENT_PAGE = ImageTemplate(templatePath=IMAGES_DIR + "soloEnchantment/个人突破页面.png",
                                      describe="个人突破页面")
