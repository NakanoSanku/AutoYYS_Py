import adbutils
from pywebio import output, start_server, pin, input
from minidevice import Minitouch, Minicap, ADBtouch, ADBcap, DroidCast
from pywebio.input import NUMBER

from src.utils.windows import WinCap, WinTouch
from pygamescript import GameScript

SCREENSHOT_METHOD = {
    'DroidCast': DroidCast,
    'minicap': Minicap,
    'adb': ADBcap,
    'windows': WinCap,
}
TOUCH_METHOD = {
    'minitouch': Minitouch,
    'adb': ADBtouch,
    'windows': WinTouch,
}
defaultTaskList = ['单人挑战', '组队挑战', '斗技', '探索', '个人突破', '寮突', '契灵']
taskList = []
device = None
handle = None


def main():
    def connect():
        global device
        global handle
        if device is not None:
            output.toast("设备已连接,请先断开连接", color='error')
            return
        if pin.pin['screenshotMethod'] is not None and pin.pin['touchMethod'] is not None:
            if (pin.pin['screenshotMethod'] == 'windows' or pin.pin['touchMethod'] == 'windows') and handle is None:
                output.toast(content="请输入windows窗口句柄")
                handle = input.input(label='请输入窗口句柄')

            screenshotMethod = SCREENSHOT_METHOD[pin.pin['screenshotMethod']]
            touchMethod = TOUCH_METHOD[pin.pin['touchMethod']]
            if pin.pin['windowHandle'] is not None:
                if pin.pin['screenshotMethod'] == 'windows':
                    screenshotMethod = SCREENSHOT_METHOD[pin.pin['screenshotMethod']](handle)
                if pin.pin['touchMethod'] == 'windows':
                    touchMethod = TOUCH_METHOD[pin.pin['touchMethod']](handle)

            if not (pin.pin['screenshotMethod'] == 'windows' and pin.pin['touchMethod'] == 'windows'):
                device = GameScript(serial=pin.pin['deviceSerial'], capMethod=screenshotMethod, touchMethod=touchMethod)
            else:
                device = GameScript(capMethod=screenshotMethod, touchMethod=touchMethod)

    def disconnect():
        global device
        if device is None:
            output.toast("设备未连接,请先连接设备", color='error')
            return
        device = None
        output.toast("设备已断开连接", color='info')

    def getDeviceList():
        pin.pin_update("deviceSerial", options=[x.serial for x in adbutils.adb.device_list()])
        output.toast("设备列表已更新", color='info')

    def deleteTask(task_id):
        global taskList
        taskList = [task for task in taskList if task['id'] != task_id]
        output.remove(scope='task' + str(task_id))

    def addTask():
        task = pin.pin['currentTask']
        times = pin.pin['times']
        task_id = len(taskList)
        taskList.append({'task': task, 'times': times, 'id': task_id})

        with output.use_scope(name='taskList') as scope_name:
            output.put_scope(name='task' + str(task_id),
                             content=output.put_row(content=[
                                 output.put_text(task),
                                 output.put_button(label="删除", onclick=lambda: deleteTask(task_id))
                             ]))

    output.put_tabs([

        {'title': '设备连接', 'content': [output.put_row(content=[
            pin.put_select('screenshotMethod',
                           options=['DroidCast', 'minicap', 'adb', 'windows'],
                           label='请选择截图方法'),
            pin.put_select('touchMethod',
                           options=['minitouch', 'adb', 'windows'],
                           label='请选择操作方法'),
            pin.put_select('deviceSerial', options=[x.serial for x in adbutils.adb.device_list()], label='请选择设备'),
        ]),
            output.put_button(label="刷新设备列表", onclick=getDeviceList),
            output.put_button(label="连接设备", onclick=connect),
            output.put_button(label="断开连接", onclick=disconnect)
        ]},

        {'title': '功能配置', 'content': output.put_markdown('~~Strikethrough~~')},

        {'title': '任务列表', 'content': [output.put_scope(name='taskList')]},

    ])
    pin.put_select('currentTask', options=defaultTaskList, label='请选择任务'),
    pin.put_input('times', type=NUMBER, label="请输入执行次数", value='999')
    output.put_button(label="添加任务", onclick=addTask),


if __name__ == '__main__':
    start_server(main, debug=True, port=8080, auto_open_webbrowser=True)
