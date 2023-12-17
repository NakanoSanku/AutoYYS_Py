import time

from loguru import logger
from pygamescript import GameScript
from src.tasks.base.collaboration.assets import ACCEPT,REJECT


def collaboration(device: GameScript, isAccept=False):
    """协作"""
    if isAccept:
        device.findAndClick(ACCEPT)
    else:
        device.findAndClick(REJECT)

