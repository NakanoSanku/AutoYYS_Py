import time
from ctypes import windll, byref, c_ubyte
from ctypes.wintypes import RECT, HWND

import cv2
import numpy as np
from minidevice import Touch, ScreenCap

PostMessageW = windll.user32.PostMessageW
ClientToScreen = windll.user32.ClientToScreen
WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x202
WM_MOUSEWHEEL = 0x020A
WHEEL_DELTA = 120
GetDC = windll.user32.GetDC
CreateCompatibleDC = windll.gdi32.CreateCompatibleDC
GetClientRect = windll.user32.GetClientRect
CreateCompatibleBitmap = windll.gdi32.CreateCompatibleBitmap
SelectObject = windll.gdi32.SelectObject
BitBlt = windll.gdi32.BitBlt
SRCCOPY = 0x00CC0020
GetBitmapBits = windll.gdi32.GetBitmapBits
DeleteObject = windll.gdi32.DeleteObject
ReleaseDC = windll.user32.ReleaseDC

# 排除缩放干扰
windll.user32.SetProcessDPIAware()


class WinCap(ScreenCap):
    def __init__(self, handle: HWND):
        self.handle = handle

    def screencap_raw(self) -> bytes:
        """
        截取窗口的屏幕截图并以字节流的形式返回
        仅支持遮挡窗口，不支持最小化窗口,速度极快,部分应用会屏蔽

        Returns:
            bytes: 截图的字节数据
        """

        r = RECT()
        GetClientRect(self.handle, byref(r))
        width, height = r.right, r.bottom
        if width <= 0 or height <= 0:
            raise ValueError("窗口客户区域大小不正确")
        # 开始截图
        dc = GetDC(self.handle)
        cdc = CreateCompatibleDC(dc)
        bitmap = CreateCompatibleBitmap(dc, width, height)
        SelectObject(cdc, bitmap)
        BitBlt(cdc, 0, 0, width, height, dc, 0, 0, SRCCOPY)
        # 截图是BGRA排列，因此总元素个数需要乘以4
        total_bytes = width * height * 4
        buffer = bytearray(total_bytes)
        byte_array = c_ubyte * total_bytes
        GetBitmapBits(bitmap, total_bytes, byte_array.from_buffer(buffer))
        DeleteObject(bitmap)
        DeleteObject(cdc)
        ReleaseDC(self.handle, dc)
        # 返回截图数据为numpy.ndarray
        image = np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)
        success, encoded_image = cv2.imencode('.jpg', image)
        if success:
            imageData = np.array(encoded_image).tobytes()
        else:
            raise Exception("图片转化失败")
        return imageData


class WinTouch(Touch):
    """
    基于Windows的触摸操作 支持最小化或后台操作，操作过程中请勿操作窗口
    """

    def __init__(self, handle: HWND):
        self.handle = handle

    def click(self, x: int, y: int, duration: int = 100):
        self._move_to(x, y)
        self._left_down(x, y)
        time.sleep(duration / 1000)
        self._left_up(x, y)

    def swipe(self, points: list, duration: int = 300):
        # TODO: 滑动大有问题
        self._left_down(points[0][0], points[0][1])
        for point in points[1:]:
            time.sleep(duration / len(points) / 1000)
            self._move_to(point[0], point[1])
        self._left_up(points[-1][0], points[-1][1])

    def _move_to(self, x: int, y: int):
        """移动鼠标到坐标（x, y)

        Args:
            handle (HWND): 窗口句柄
            x (int): 横坐标
            y (int): 纵坐标
        """
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-mousemove
        wparam = 0
        lparam = y << 16 | x
        PostMessageW(self.handle, WM_MOUSEMOVE, wparam, lparam)

    def _left_down(self, x: int, y: int):
        """在坐标(x, y)按下鼠标左键

        Args:
            handle (HWND): 窗口句柄
            x (int): 横坐标
            y (int): 纵坐标
        """
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-lbuttondown
        wparam = 0
        lparam = y << 16 | x
        PostMessageW(self.handle, WM_LBUTTONDOWN, wparam, lparam)

    def _left_up(self, x: int, y: int):
        """在坐标(x, y)放开鼠标左键

        Args:
            handle (HWND): 窗口句柄
            x (int): 横坐标
            y (int): 纵坐标
        """
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-lbuttonup
        wparam = 0
        lparam = y << 16 | x
        PostMessageW(self.handle, WM_LBUTTONUP, wparam, lparam)


if __name__ == "__main__":
    win = WinCap(0x6039E)
    win.save_screencap()
    #性能很强，但同时只能使用dx模式渲染模拟器，模拟器占用非常高
    # from ctypes import windll, byref, c_ubyte
    # from ctypes.wintypes import RECT, HWND
    # import numpy as np
    #
    # GetDC = windll.user32.GetDC
    # CreateCompatibleDC = windll.gdi32.CreateCompatibleDC
    # GetClientRect = windll.user32.GetClientRect
    # CreateCompatibleBitmap = windll.gdi32.CreateCompatibleBitmap
    # SelectObject = windll.gdi32.SelectObject
    # BitBlt = windll.gdi32.BitBlt
    # SRCCOPY = 0x00CC0020
    # GetBitmapBits = windll.gdi32.GetBitmapBits
    # DeleteObject = windll.gdi32.DeleteObject
    # ReleaseDC = windll.user32.ReleaseDC
    #
    # # 排除缩放干扰
    # windll.user32.SetProcessDPIAware()
    #
    #
    # def capture(handle: HWND):
    #     """窗口客户区截图
    #
    #     Args:
    #         handle (HWND): 要截图的窗口句柄
    #
    #     Returns:
    #         numpy.ndarray: 截图数据
    #     """
    #     # 获取窗口客户区的大小
    #     r = RECT()
    #     GetClientRect(handle, byref(r))
    #     width, height = r.right, r.bottom
    #     # 开始截图
    #     dc = GetDC(handle)
    #     cdc = CreateCompatibleDC(dc)
    #     bitmap = CreateCompatibleBitmap(dc, width, height)
    #     SelectObject(cdc, bitmap)
    #     BitBlt(cdc, 0, 0, width, height, dc, 0, 0, SRCCOPY)
    #     # 截图是BGRA排列，因此总元素个数需要乘以4
    #     total_bytes = width * height * 4
    #     buffer = bytearray(total_bytes)
    #     byte_array = c_ubyte * total_bytes
    #     GetBitmapBits(bitmap, total_bytes, byte_array.from_buffer(buffer))
    #     DeleteObject(bitmap)
    #     DeleteObject(cdc)
    #     ReleaseDC(handle, dc)
    #     # 返回截图数据为numpy.ndarray
    #     return np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)
    #
    #
    # handle = windll.user32.FindWindowW(None, "QQ")
    # image = capture(0x6039E)
    # cv2.imshow("Capture Test", image)
    # cv2.waitKey()
