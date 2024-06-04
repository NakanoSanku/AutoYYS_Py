import threading

import cv2
import numpy as np
from pygamescript import Template

from src.config import OCR_PATH
from src.utils.RapidOCR_api import OcrAPI
from src.utils.decorators import synchronized


def showAllResult():
    return OcrTemplate.cache


class OcrTemplate(Template):
    ocr = None
    ocrLock = threading.Lock()
    cache = None

    def __init__(
        self,
        text: str,
        threshold=0.8,
        region: list = None,
        isGary=False,
        useCache=False,
    ) -> None:
        self.text = text  # 初始化文本属性，text为输入的字符串
        self.threshold = threshold  # 初始化阈值属性，threshold为默认值0.8
        self.region = region  # 初始化区域属性，region为传入的列表，默认为None
        self.isGary = isGary  # 初始化是否为Gary属性，isGary默认为False
        self.useCache = useCache  # 是否使用之前的结果

    @synchronized(ocrLock)
    def match(self, image):
        self.start()
        x_min, y_min, x_max, y_max = self.region or (
            0,
            0,
            image.shape[1],
            image.shape[0],
        )
        if not self.useCache:
            image = image[y_min:y_max, x_min:x_max]
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if self.isGary else image
            success, encoded_image = cv2.imencode(".jpg", image)
            if success:
                imageData = np.array(encoded_image).tobytes()
            else:
                raise Exception("图片转化失败")
            OcrTemplate.cache = self.ocr.runBytes(imageData)
        if OcrTemplate.cache.get("code", 0) == 100:
            matched_regions = [
                item
                for item in OcrTemplate.cache.get("data", [])
                if item.get("text", "") == self.text
                and item.get("score", 0) > self.threshold
            ]
            for item in matched_regions:
                x1, y1, x2, y2 = item["box"][0] + item["box"][2]
                return [x1 + x_min, y1 + y_min, x2 + x_min, y2 + y_min]
        return None

    def __str__(self) -> str:
        return self.text

    def __del__(self):
        if OcrTemplate.ocr is not None:
            OcrTemplate.ocr.stop()

    @staticmethod
    def stop():
        if OcrTemplate.ocr is not None:
            OcrTemplate.ocr.stop()

    @staticmethod
    def start(config: str = None):
        if config is None:
            config = "--numThread=1"
        if OcrTemplate.ocr is None:
            OcrTemplate.ocr = (
                OcrAPI(OCR_PATH) if config is None else OcrAPI(OCR_PATH, config)
            )
