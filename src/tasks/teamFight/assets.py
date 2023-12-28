from pygamescript import ImageTemplate, ColorsTemplate

from src.config import IMAGES_DIR

TEAM_FIGHT = ImageTemplate(templatePath=IMAGES_DIR + "/teamFight/TEAM_FIGHT.png", describe="多人挑战按钮")
THREE_PLAYER = ColorsTemplate("#fffffe",
                              [[14, 1, "#fffffe"], [20, 1, "#ffffff"], [31, 1, "#fffffe"],
                               [37, 1, "#fffffe"], [17, -15, "#fffeee"], [21, -6, "#fffffa"]],
                              "三人组队",
                              [997, 150, 1191, 354])
