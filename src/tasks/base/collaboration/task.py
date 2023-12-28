
from pygamescript import GameScript

from src.tasks.base.baseTask import BaseTask
from src.tasks.base.collaboration.assets import ACCEPT, REJECT


class CollaborationTask(BaseTask):
    def __str__(self):
        return f"协作任务"

    def __init__(self, device: GameScript, isAccept=False):
        self.device = device
        self.isAccept = isAccept

    def run(self):
        """协作"""
        if self.isAccept:
            self.device.findAndClick(ACCEPT)
        else:
            self.device.findAndClick(REJECT)
