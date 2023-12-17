from pygamescript import *
from adbutils import adb

from src.tasks.explore.task import explore
from src.tasks.soloEnchantment.task import soloEnchantment
import loguru

ld = GameScript(adb.device_list()[0].serial, DroidCast, Minitouch)
loguru.logger.disable('minidevice')
# explore(ld, 120)
soloEnchantment(ld)
