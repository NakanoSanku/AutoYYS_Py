import time

import loguru
from pygamescript import GameScript

from src.tasks.base.enterEnchantment.assets import SOLO_ENCHANTMENT, ENCHANTMENT, HUT_ENCHANTMENT


def enterEnchantment(device: GameScript, enchantmentType: ['个突', '寮突'] = '个突'):
    while True:
        if enchantmentType == '寮突':
            if device.findAndClick(HUT_ENCHANTMENT):
                break
        elif enchantmentType == '个突':
            if device.findAndClick(SOLO_ENCHANTMENT):
                break
        device.findAndClick(ENCHANTMENT)
        time.sleep(0.5)

    loguru.logger.info(f"{enchantmentType}界面")
