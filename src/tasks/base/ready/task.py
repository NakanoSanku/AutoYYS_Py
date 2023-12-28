from time import sleep

from pygamescript import GameScript

from src.tasks.base.ready.assets import READY, EXIT_CONFIRM, EXIT, PRESET_GROUP_UNSELECTED, PRESET_GROUP_REGION, \
    PRESET_SELECTED, PRESET_REGION, PLAYING, PRESET, PRESET_BUTTON_REGION, PRESET_PAGE, PLAY_BUTTON
from src.tasks.base.baseTask import BaseTask


class ReadyTask(BaseTask):
    def __init__(self, device: GameScript, isExit=False, isChangePreset=False, presetGroup: int = None,
                 presetIndex: int = None) -> None:
        """准备阶段任务模块

        Args:
            device (GameScript): _description_
            isExit (bool, optional): _description_. Defaults to False.
            isChangePreset (bool, optional): _description_. Defaults to False.
            presetGroup (int, optional): _description_. Defaults to None.
            presetIndex (int, optional): _description_. Defaults to None.
        """
        self.device = device
        self.isExit = isExit
        self.isChangePreset = isChangePreset
        if isChangePreset:
            self.presetGroup = presetGroup
            self.presetIndex = presetIndex

    def run(self):
        result = self.device.find(READY)
        if result:
            if self.isExit:
                self.__exit()
            elif self.isChangePreset:
                self.__changePreset()
                return True
            else:
                self.device.rangeRandomClick(result)

    def __exit(self):
        if not self.device.findAndClick(EXIT_CONFIRM):
            self.device.findAndClick(EXIT)

    def __changePreset(self):
        PRESET_GROUP_UNSELECTED.region = PRESET_GROUP_REGION[self.presetGroup]
        PLAYING.region = PRESET_SELECTED.region = PRESET_REGION[self.presetIndex]

        self.device.findAndClick(PRESET, result=PRESET_BUTTON_REGION)
        if self.device.find(PRESET_PAGE):
            if self.device.find(PRESET_GROUP_UNSELECTED):
                """分组未选中"""
                self.device.rangeRandomClick(PRESET_GROUP_UNSELECTED.region)
            else:
                """分组已选中"""
                if not self.device.find(PRESET_SELECTED):
                    """预设未选中"""
                    self.device.rangeRandomClick(PRESET_SELECTED.region)
                else:
                    """预设选中"""
                    if self.device.find(PLAYING):
                        """预设已出战"""
                        self.isChangePreset = False
                    else:
                        self.device.findAndClick(PLAY_BUTTON)

    def __str__(self):
        return "准备任务\n是否退出:{}\n是否换预设:{}\n预设组:{}\n预设:{}".format(self.isExit, self.isChangePreset,
                                                                                 self.presetGroup, self.presetIndex)


def ready(device: GameScript, isExit=False, isChangePreset=False, presetGroup: int = None, presetIndex: int = None):
    result = device.find(READY)
    if result:
        if isExit:
            if not device.findAndClick(EXIT_CONFIRM):
                device.findAndClick(EXIT)
        elif isChangePreset:
            changePreset(device, presetGroup, presetIndex)
            return True
        else:
            device.rangeRandomClick(result)


def changePreset(device: GameScript, presetGroup: int, presetIndex: int):
    PRESET_GROUP_UNSELECTED.region = PRESET_GROUP_REGION[presetGroup]
    PLAYING.region = PRESET_SELECTED.region = PRESET_REGION[presetIndex]
    while 1:
        device.findAndClick(PRESET, result=[45, 653, 79, 708])
        if device.find(PRESET_PAGE):
            if device.find(PRESET_GROUP_UNSELECTED):
                device.rangeRandomClick(PRESET_GROUP_UNSELECTED.region)
            if not device.find(PRESET_SELECTED):
                device.rangeRandomClick(PRESET_SELECTED.region)
            else:
                if device.find(PLAYING):
                    return
                else:
                    device.findAndClick(PLAY_BUTTON)
                    sleep(1)
                    if not device.find(PRESET_PAGE):
                        return
        sleep(1)


if __name__ == '__main__':
    from pygamescript import GameScript
    from minidevice import DroidCast, ADBtouch
    from adbutils import adb

    serial = adb.device_list()[0].serial
    ld = GameScript(serial, DroidCast, ADBtouch)


    def func():
        # device.findAndClick(CONFIRM)
        isChangePreset = True
        while 1:
            isChangePreset = False if ready(ld,
                                            isExit=False,
                                            isChangePreset=isChangePreset,
                                            presetGroup=5,
                                            presetIndex=0) else isChangePreset


    func()
