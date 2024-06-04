import threading
import time
import uuid

from src.app.Models.Task import Task


class Device:
    def __init__(self, device, interval=500):
        self.device = device
        self.taskList = {}
        self.status = -1
        self.interval = interval
        self.taskThread = None

    def start(self, isLoop=False):
        """启动任务"""
        self.status = 1

        def func():
            while self.status:
                task = self.nextTask()
                if task is None:
                    if isLoop:
                        self.resetTaskList(self.device)  # 重置任务列表
                    else:
                        break
                else:
                    task.ex.run()
                time.sleep(self.interval / 1000)

        if self.taskThread is None:
            self.taskThread = threading.Thread(target=func, name="Task")
            self.taskThread.start()

    def stop(self):
        """停止任务"""
        self.pause()
        self.resetTaskList(self.device)  # 重置任务列表

    def pause(self):
        self.status = 0
        self.taskThread = None

    def nextTask(self):
        """获取下一个任务uuid"""
        for label, value in self.taskList.items():
            if value.ex.done:
                value.status = 1
            if value.status != 1:
                value.status = 0  # 更新任务运行状态为运行中
                return value
        return None

    def addTask(self, task: Task):
        """添加任务"""
        # 初始化任务
        task.createTaskEx(self.device)
        # 添加任务对象到实例任务列表
        # 获取任务UUID
        taskUUID = str(uuid.uuid4())
        self.taskList[taskUUID] = task
        return taskUUID

    def delTask(self, taskUUID: str):
        """根据uuid删除任务"""
        if taskUUID in self.taskList:
            del self.taskList[taskUUID]
            return True
        return False

    def resetTaskList(self, device):
        """
        Resets the task list 重置任务列表
        """
        for key, value in self.taskList.items():
            value.status = -1
            value.createTaskEx(device)
        return True
