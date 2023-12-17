import time

from loguru import logger
from pygamescript import GameScript
from src.tasks.base.enchantmentFight.assets import ATTACK, PINK_X


def enchantmentFight(device: GameScript):
    if device.findAndClick(ATTACK):
        time.sleep(3)
        if device.find(ATTACK):
            """退出至探索界面"""
            while True:
                if device.findAndClick(PINK_X):
                    time.sleep(3)
                    if not device.find(PINK_X):
                        return True
                time.sleep(0.5)
