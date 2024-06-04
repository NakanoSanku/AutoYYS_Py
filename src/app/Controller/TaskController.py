# 用于控制任务类请请求处理
from flask import Blueprint, request, current_app
from pygamescript import Template

from src.app import TASKS, TASKS_MAP
from src.app.Models.InvaidUsage import InvalidUsage
from src.app.Models.ResponseResult import success_response
from src.app.Models.Task import Task

taskController = Blueprint('taskController', __name__)


@taskController.route('/getTaskList')
def getTaskList():
    return success_response(data=TASKS)


@taskController.route('/addTask', methods=['POST'])
def addTask():
    data = request.json
    uuid = data.get("uuid")
    task = data.get("task")
    config = data.get("config", {})
    if task not in TASKS:
        raise InvalidUsage(message="Task not found")
    if uuid not in current_app.config["device_map"]:
        raise InvalidUsage(message="Device Not Found")
    taskUUID = current_app.config["device_map"][uuid].addTask(Task(task, config))
    return success_response(data=taskUUID)


@taskController.route('/delTask', methods=['POST'])
def delTask():
    data = request.json
    uuid = data.get("uuid")
    taskUUID = data.get("taskUUID")
    if uuid not in current_app.config["device_map"]:
        raise InvalidUsage(message="Device Not Found")
    if taskUUID not in current_app.config["device_map"][uuid].taskList:
        raise InvalidUsage(message="Task Not Found")
    result = current_app.config["device_map"][uuid].delTask(taskUUID)
    return success_response(data=result)


@taskController.route('/startTask', methods=['POST'])
def startTask():
    data = request.json
    uuid = data.get("uuid")
    isLoop = data.get("isLoop")
    if uuid not in current_app.config["device_map"]:
        raise InvalidUsage(message="Device Not Found")
    current_app.config["device_map"][uuid].start(isLoop)
    return success_response()


@taskController.route('/stopTask', methods=['POST'])
def stopTask():
    data = request.json
    uuid = data.get("uuid")
    if uuid not in current_app.config["device_map"]:
        raise InvalidUsage(message="Device Not Found")
    current_app.config["device_map"][uuid].stop()
    return success_response()


@taskController.route('/pauseTask', methods=['POST'])
def pauseTask():
    data = request.json
    uuid = data.get("uuid")
    if uuid not in current_app.config["device_map"]:
        raise InvalidUsage(message="Device Not Found")
    current_app.config["device_map"][uuid].pause()
    return success_response()


@taskController.route('/getDeviceTaskList', methods=['POST'])
def getDeviceTaskList():
    data = request.json
    uuid = data.get("uuid")
    if uuid not in current_app.config["device_map"]:
        raise InvalidUsage(message="Device Not Found")
    tmpList = current_app.config["device_map"][uuid].taskList
    taskStrList = [({**task.getStatus(), **{"uuid": key}}) for key, task in
                   tmpList.items()]
    return success_response(data=taskStrList)


@taskController.route("/getTaskConfig")
def getTaskConfig():
    task = request.args.get("task")
    config = TASKS_MAP[task].defaultConfig
    configList = {}
    for key, value in config.items():
        if not isinstance(value, Template):
            configList.update({key: value})
    return success_response(data=configList)
