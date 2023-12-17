import time

from loguru import logger
from pygamescript import GameScript
from src.tasks.changeSoul.assets import *


def openTeamDefault(device: GameScript):
    while True:
        if device.find(PRESET_2, isColor=True, colorThreshold=15):
            return True
        device.findAndClick(SHIIKSA)
        device.findAndClick(PRESET)
        time.sleep(1)


def selectTeam(device: GameScript, group, team):
    APPLY_PRESET.region = TEAM_REGION_LIST[team]
    COLORS_TEMPLATE.region = GROUP_REGION_LIST[group]
    time.sleep(2)
    while True:
        if device.find(COLORS_TEMPLATE):
            break
        device.rangeRandomClick(result=GROUP_REGION_LIST[group])
        time.sleep(2)
    device.findAndClick(APPLY_PRESET)
    time.sleep(2)
    device.findAndClick(CONFIRM)
    time.sleep(2)
    while True:
        if device.findAndClick(EXIT):
            time.sleep(2)
            if not device.find(EXIT):
                return


def changeSoul(device: GameScript, group, team):
    openTeamDefault(device)
    selectTeam(device,group,team)
