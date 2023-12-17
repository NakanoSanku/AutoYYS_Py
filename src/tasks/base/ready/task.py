from pygamescript import GameScript

from src.tasks.base.ready.assets import READY, EXIT, EXIT_CONFIRM


def ready(device: GameScript, isExit=False):
    result = device.find(READY)
    if result:
        if isExit:
            if not device.findAndClick(EXIT_CONFIRM):
                device.findAndClick(EXIT)
        else:
            device.rangeRandomClick(result)
