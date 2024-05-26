from minidevice import DroidCast, MiniCap, ADBCap, ADBTouch, MiniTouch, MaaTouch
from minidevicemumuapi import MuMuScreenCap, MuMuTouch

from src.app.Service.tasks import Explore, PersonalBreakthrough, FightSkill, SingleFight, TeamFight, SecretStory, \
    SixStreet, \
    EnterScene, RegionalGhostKing, DevilTime, Dogoate, ToiletPaper
from src.utils.windows import WinCap, WinTouch

SCREENSHOT_METHODS_MAP = {
    "DroidCast": DroidCast,
    "MiniCap": MiniCap,
    "ADB": ADBCap,
    "Windows": WinCap,
    "MuMu": MuMuScreenCap
}

TOUCH_METHODS_MAP = {
    "ADB": ADBTouch,
    "MiniTouch": MiniTouch,
    'MaaTouch': MaaTouch,
    "Windows": WinTouch,
    "MuMu": MuMuTouch,
}

TASKS_MAP = {
    "探索": Explore,
    "个突": PersonalBreakthrough,
    "斗技": FightSkill,
    "六道-椒图": SixStreet,
    "组队战斗": TeamFight,
    "抽厕纸": ToiletPaper,
    "秘闻竞速": SecretStory,
    "地域鬼王": RegionalGhostKing,
    "逢魔之时": DevilTime,
    "单人挑战": SingleFight,
    "道馆": Dogoate,
}

SCREENSHOT_METHODS = list(SCREENSHOT_METHODS_MAP.keys())
TOUCH_METHODS = list(TOUCH_METHODS_MAP.keys())
TASKS = list(TASKS_MAP.keys())
