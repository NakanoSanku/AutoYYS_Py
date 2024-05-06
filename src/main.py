import time

import loguru
from adbutils import adb
from minidevice import DroidCast, MiniTouch, MiniCap, ADBCap, ADBTouch, MaaTouch
from pygamescript import GameScript

from src.tasks import SecretStory
# from src.utils.windows import WinCap, WinTouch

CAP_METHODS = {
    "DroidCast": DroidCast,
    "MiniCap": MiniCap,
    "ADB": ADBCap,
    # "Windows": WinCap
}
TOUCH_METHODS = {
    "ADB": ADBTouch,
    "MiniTouch": MiniTouch,
    'MaaTouch': MaaTouch
    # "Windows": WinTouch
}


def getDeviceList():
    return [device.serial for device in adb.device_list()]


loguru.logger.disable("minidevice")
loguru.logger.level("INFO")
print("六道测试用例")
device = None
deviceList = getDeviceList()
for i, device in enumerate(deviceList):
    print("{}-{}".format(i, device))
deviceId = input("选择连接设备: ")
print("等待设备连接")
device = GameScript(serial=deviceList[int(deviceId)], capMethod=DroidCast, touchMethod=MiniTouch)
print("设备连接完成")

task = SecretStory(device)

while 1:
    task.run()
    time.sleep(0.5)
    if task.done:
        break

print("任务完成")
