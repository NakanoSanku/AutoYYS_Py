import time

from loguru import logger
from pygamescript import GameScript
from src.tasks.base.inviteTeam.assets import ACCEPT, AUTO_ACCEPT, REJECT


def inviteTeam(device: GameScript, isAccept=False):
    """组队邀请"""
    if isAccept:
        if not device.findAndClick(AUTO_ACCEPT):
            device.findAndClick(ACCEPT)
    else:
        device.findAndClick(REJECT)
