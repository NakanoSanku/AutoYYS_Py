import time

from loguru import logger
from pygamescript import GameScript
from src.tasks.changePreset.assets import *


def changePreset(device: GameScript, group, team):
    COLORS_TEMPLATE.region = GROUP_REGION_LIST[group]

    while True:
        if device.find(READY):
            if device.find(PRESET_SWIPE):
                break
            device.rangeRandomClick(result=[46, 655, 79, 708])
            time.sleep(2)
    time.sleep(2)
    while True:
        if device.find(COLORS_TEMPLATE):
            break
        device.rangeRandomClick(GROUP_REGION_LIST[group])
        time.sleep(2)
    time.sleep(2)
    device.rangeRandomClick(TEAM_REGEION_LIST[team])
    time.sleep(2)
    device.findAndClick(CONFIRM)
    while True:
        if device.findAndClick(READY):
            time.sleep(2)
            if not device.find(READY):
                return
