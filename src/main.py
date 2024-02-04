import time

import loguru
from pygamescript import GameScript
from minidevice import DroidCast, MiniTouch, MiniCap, ADBCap, ADBTouch, MaaTouch
from adbutils import adb

from src.tasks import SixStreet

# from src.utils.windows import WinCap, WinTouch

CAP_METHODS = {
    "DroidCast": DroidCast,
    "Minicap": MiniCap,
    "ADB": ADBCap,
    # "Windows": WinCap
}
TOUCH_METHODS = {
    "ADB": ADBTouch,
    "minitouch": MiniTouch,
    'MaaTouch': MaaTouch,
    # "Windows": WinTouch
}


def getDeviceList():
    return [device.serial for device in adb.device_list()]


loguru.logger.level("INFO")
print("六道测试用例")
device = None
deviceList = getDeviceList()
for i, device in enumerate(deviceList):
    print("{}-{}".format(i, device))
deviceId = input("选择连接设备: ")
print("等待设备连接")
device = GameScript(serial=deviceList[int(deviceId)], capMethod=DroidCast, touchMethod=MaaTouch)
print("设备连接完成")

task = SixStreet(device, 99)

while 1:
    task.run()
    time.sleep(0.5)
    print("执行中")
    if task.done:
        break

print("任务完成")
