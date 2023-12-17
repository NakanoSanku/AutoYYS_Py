from pygamescript import *

from src.config import IMAGES_DIR

AUTO_ACCEPT = ImageTemplate(templatePath=IMAGES_DIR + "/inviteTeam/AUTO_ACCEPT.png", describe="自动接受组队邀请")
ACCEPT = ImageTemplate(templatePath=IMAGES_DIR + "/inviteTeam/ACCEPT.png", describe="接受组队邀请")
REJECT = ImageTemplate(templatePath=IMAGES_DIR + "/inviteTeam/REJECT.png", describe="拒绝组队邀请")
