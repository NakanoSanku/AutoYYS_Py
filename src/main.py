# encoding:utf-8
import time

import loguru
from pygamescript import GameScript
from minidevice import Minitouch, DroidCast
from adbutils import adb
from apscheduler.schedulers.background import BackgroundScheduler
from src.tasks.explore.task import ExploreTask
from src.tasks.soloEnchantment.task import SoloEnchantmentTask
from src.tasks.teamFight.task import TeamFight
from src.tasks.base.collaboration.task import CollaborationTask

my_token = "41cdfb44e148403ca067fa2b74c01282"

loguru.logger.disable("minidevice")
device = adb.device_list()[0].serial
ld = GameScript(device, capMethod=DroidCast, touchMethod=Minitouch)
task1 = ExploreTask(ld, 10)
task2 = SoloEnchantmentTask(ld, is_ensure_level=True)

task3 = TeamFight(ld, 999, isLeader=True)
task4 = CollaborationTask(ld, isAccept=True)
sche = BackgroundScheduler()
exploreTask = sche.add_job(task3.run, 'interval', seconds=0.5)
sche.add_job(task4.run, 'interval', seconds=5)
if __name__ == '__main__':
    sche.start()
    while True:
        time.sleep(1)
        if task2.done:
            print('任务完成')
            break
