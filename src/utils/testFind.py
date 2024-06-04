# 用于测试图片是否能够被正常识别
import time

import cv2
import minicv
from pygamescript import Template,GameScript

from src.app.Service.tasks import PersonalBreakthrough


# test_performance.py


def testFind(taskClass, screenshot):
    for key, value in taskClass.defaultConfig.items():
        if isinstance(value, Template):
            s = time.time()
            result = value.match(screenshot)
            if result:
                cv2.rectangle(screenshot, (result[0], result[1]), (result[2], result[3]), (0, 0, 255), 2)
            print(result, value)
            print(time.time() - s)
    minicv.Images.save(screenshot, "结果保存_{}.jpg".format(time.time()))


if __name__ == '__main__':
    test = GameScript("127.0.0.1:")
    # for i in range(100):
    #     testFind(taskClass=PersonalBreakthrough)
    #     time.sleep(0.5)
