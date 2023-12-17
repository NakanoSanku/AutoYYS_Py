from pygamescript import *

from src.config import IMAGES_DIR

FIGHT_SKILL_FIGHT = ImageTemplate(templatePath=IMAGES_DIR + "/fightSkill/FIGHT_SKILL_FIGHT.png",
                                  describe="斗技挑战按钮",
                                  threshold=0.7)

FIGHT_SKILL_GO_INTO_BATTLE = ImageTemplate(templatePath=IMAGES_DIR + "/fightSkill/FIGHT_SKILL_GO_INTO_BATTLE.png",
                                           describe="自动上阵按钮",
                                           threshold=0.8)
