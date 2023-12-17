import customtkinter
from adbutils import adb


class MyTabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("任务列表")
        self.add("设置界面")
        self.add("日志系统")
        self.add("设备控制")


TASKS_LIST = ["御魂", "探索", "个人突破"]


class MyScrollableFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


class SettingFrame(customtkinter.CTkFrame):
    """设置界面"""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


class LoggingFrame(customtkinter.CTkScrollableFrame):
    """日志界面"""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


class DeviceControlFrame(customtkinter.CTkFrame):
    """设备控制界面"""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.connectDevice = None
        # 选择设备列表
        self.adbDevice = customtkinter.StringVar(value="")
        self.adbDeviceList = customtkinter.CTkOptionMenu(self, values=[device.serial for device in adb.device_list()],
                                                         command=self.adbDeviceList_callback,
                                                         variable=self.adbDevice)
        self.adbDeviceList.grid(row=1, column=0, padx=2, pady=2)
        # 刷新设备列表
        self.refreshButton = customtkinter.CTkButton(self, text="Refresh Device List",
                                                     command=self.refreshButton_callback)
        self.refreshButton.grid(row=1, column=1, padx=2, pady=2)
        # 连接设备
        self.connectButton = customtkinter.CTkButton(self, text="Connect Device", command=self.connectButton_callback)
        self.connectButton.grid(row=2, column=0, padx=2, pady=2)

        # 断开设备
        self.disconnectButton = customtkinter.CTkButton(self, text="Disconnect Device",
                                                        command=self.disconnectButton_callback)
        self.disconnectButton.grid(row=2, column=1, padx=2, pady=2)

    def refreshButton_callback(self):
        self.adbDeviceList.destroy()
        self.adbDevice = customtkinter.StringVar(value="")
        self.adbDeviceList = customtkinter.CTkOptionMenu(self, values=[device.serial for device in adb.device_list()],
                                                         command=self.adbDeviceList_callback,
                                                         variable=self.adbDevice)
        self.adbDeviceList.grid(row=1, column=0, padx=2, pady=2)

    def connectButton_callback(self):
        if self.adbDevice != "":
            """连接设备逻辑"""
            print(self.adbDevice)
            # self.connectDevice = adb.device(self.adbDevice)

    def disconnectButton_callback(self):
        if self.connectDevice is not None:
            """断开设备逻辑"""
            self.connectDevice = None

    def adbDeviceList_callback(self, choice):
        self.adbDevice = choice


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.taskRunList = []
        self.taskLabelList = None

        self.tab_view = MyTabView(master=self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20)

        self.taskRunListFrame = MyScrollableFrame(self.tab_view.tab("任务列表"))
        self.taskRunListFrame.grid(row=0, column=0, padx=2, pady=2)

        self.taskRunListFrame = DeviceControlFrame(self.tab_view.tab("设备控制"))
        self.taskRunListFrame.grid(row=0, column=0, padx=2, pady=2)

        # 选择任务列表
        self.task = customtkinter.StringVar(value="")
        self.tasksList = customtkinter.CTkOptionMenu(self, values=TASKS_LIST,
                                                     command=self.tasksList_callback,
                                                     variable=self.task)
        self.tasksList.grid(row=5, column=0, padx=2, pady=2)
        # 添加任务
        self.addTaskButton = customtkinter.CTkButton(self, text="Add Task",
                                                     command=self.addTaskButton_callback)
        self.addTaskButton.grid(row=6, column=0, padx=2, pady=2)

    def button_callback(self):
        print("button clicked")

    def tasksList_callback(self, choice):
        self.task = choice

    def addTaskButton_callback(self):
        self.taskRunList.append(self.task)
        self.taskLabelList = [customtkinter.CTkLabel(self.taskRunListFrame, text=str(task)) for task in
                              self.taskRunList]
        for label, i in zip(self.taskLabelList, range(len(self.taskLabelList))):
            label.grid(row=i, column=0, padx=2, pady=2)

        print(self.taskRunList)
        # self.connectDevice = adb.device(self.adbDevice)

    def refreshTabs(self):
        self.tab_view.destroy()
        self.tab_view = MyTabView(master=self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20)


if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    app = App()
    app.mainloop()
