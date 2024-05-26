import os

PROJECT_NAME = "AutoYYS_Py"


def getRootPath():
    curPath = os.path.abspath(os.path.abspath(__file__))
    return curPath[:curPath.find(PROJECT_NAME) + len(PROJECT_NAME)] + '/'


# 设置项目根目录的全局变量
ROOT_DIR = getRootPath()
ASSETS_DIR = ROOT_DIR + "assets/"
IMAGES_DIR = ASSETS_DIR + "images/"
OCR_PATH = ASSETS_DIR + "bin/ocr/RapidOCR-json.exe"
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
