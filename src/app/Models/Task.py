from src.app import TASKS_MAP


class Task:
    def __init__(self, name, config):
        self.name = name
        self.config = config
        self.status = -1
        self.ex = None

    def createTaskEx(self, device):
        self.ex = TASKS_MAP[self.name](device, self.config)

    def __str__(self):
        return "Task " + self.name

    def getStatus(self):
        return {
            "name": self.name,
            "config": self.config,
            "status": self.status,
            "ex": self.ex
        }
