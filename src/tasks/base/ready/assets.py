from pygamescript import ImageTemplate, ColorsTemplate

from src.config import IMAGES_DIR

READY = ImageTemplate(
    templatePath=IMAGES_DIR + "准备/准备按钮.png",
    describe="准备按钮",
    region=[1000, 500, 1280, 720])

EXIT = ImageTemplate(
    templatePath=IMAGES_DIR + "准备/退出战斗.png",
    describe="退出战斗",
    region=[0, 0, 100, 100])

EXIT_CONFIRM = ImageTemplate(
    templatePath=IMAGES_DIR + "准备/退出战斗确认.png",
    describe="退出确认",
    region=[650, 350, 850, 500])

PRESET = ColorsTemplate(
    firstColor="#d97465",
    colors=[[-2, 10, "#de816e"], [-2, 22, "#e08572"], [0, 31, "#de7a69"],
            [7, 12, "#fffaf1"], [36, 8, "#de8271"], [31, -5, "#dc7363"],
            [36, 12, "#e58f77"], [37, 22, "#dd8370"], [33, 28, "#e4937c"]],
    describe="预设",
    region=[18, 624, 105, 719])

PRESET_PAGE = ColorsTemplate(
    firstColor="#dfc9b6",
    colors=[[34, 0, "#dfc9b6"], [65, 22, "#5f4637"], [39, 78, "#dfc9b6"],
            [68, 35, "#8e7851"], [68, 46, "#391f17"], [66, 40, "#4c331e"]],
    region=[618, 194, 800, 387],
    describe="预设页面",
    threshold=1
)

PRESET_GROUP_REGION = [
    [33, 237, 167, 297],
    [32, 299, 169, 363],
    [31, 363, 168, 424],
    [32, 425, 168, 487],
    [32, 490, 167, 549],
    [31, 551, 168, 614],
    [31, 616, 168, 676]
]

PRESET_REGION = [
    [194, 232, 664, 348],
    [193, 353, 665, 470],
    [193, 475, 665, 588],
]

PLAYING = ImageTemplate(
    templatePath=IMAGES_DIR + "准备/出战状态.png",
    describe="出战状态")

PLAY_BUTTON = ImageTemplate(
    templatePath=IMAGES_DIR + "准备/出战按钮.png",
    describe="出战按钮",
    region=[331, 623, 545, 714])

PRESET_GROUP_UNSELECTED = ColorsTemplate(
    firstColor="#e2d3c0",
    colors=[[43, 5, "#e1d2be"], [65, 5, "#e3d3c0"], [83, 9, "#d3bfa9"],
            [81, 30, "#e0cfbc"], [63, 38, "#dfd0bc"], [28, 42, "#d7c4b0"]],
    describe="预设分组未选中"
)

PRESET_SELECTED = ColorsTemplate(
    firstColor="#b77fc9",
    colors=[[10, 0, "#b77fc9"], [-187, -3, "#ced0f7"], [-191, -3, "#cdcff7"], [-191, 0, "#750cee"],
            [-187, 0, "#903bc6"]],
    describe="预设选中"
)

PRESET_BUTTON_REGION = [45, 653, 79, 708]

if __name__ == '__main__':
    from pygamescript import GameScript
    from minidevice import ADBcap, ADBtouch
    from adbutils import adb

    serial = adb.device_list()[0].serial
    device = GameScript(serial, ADBcap, ADBtouch)


    def func():
        device.findAndClick(PRESET_PAGE)

    func()
