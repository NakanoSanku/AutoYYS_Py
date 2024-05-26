# 用于控制任务类请请求处理
from flask import Blueprint, render_template, jsonify, request, current_app
from src.app.Models.ResponseResult import success_response, error_response
from src.app import TASKS
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
        return error_response(message="Task not found")
    if uuid not in current_app.config["device_map"]:
        return error_response(message="Device Not Found")
    taskUUID = current_app.config["device_map"][uuid].addTask(Task(task, config))
    return success_response(data=taskUUID)


@taskController.route('/delTask', methods=['POST'])
def delTask():
    data = request.json
    uuid = data.get("uuid")
    taskUUID = data.get("taskUUID")
    if uuid not in current_app.config["device_map"]:
        return error_response(message="Device Not Found")
    if taskUUID not in current_app.config["device_map"].taskList:
        return error_response(message="Task Not Found")
    result = current_app.config["device_map"][uuid].delTask(taskUUID)
    return success_response(data=result)


@taskController.route('/startTask', methods=['POST'])
def startTask():
    data = request.json
    uuid = data.get("uuid")
    if uuid not in current_app.config["device_map"]:
        return error_response(message="Device Not Found")
    current_app.config["device_map"][uuid].start()
    return success_response()


@taskController.route('/stopTask', methods=['POST'])
def stopTask():
    data = request.json
    uuid = data.get("uuid")
    if uuid not in current_app.config["device_map"]:
        return error_response(message="Device Not Found")
    current_app.config["device_map"][uuid].stop()
    return success_response()


@taskController.route('/pauseTask', methods=['POST'])
def pauseTask():
    data = request.json
    uuid = data.get("uuid")
    if uuid not in current_app.config["device_map"]:
        return error_response(message="Device Not Found")
    current_app.config["device_map"][uuid].pause()
    return success_response()


@taskController.route('/getDeviceTaskList', methods=['POST'])
def getDeviceTaskList():
    data = request.json
    uuid = data.get("uuid")
    if uuid not in current_app.config["device_map"]:
        return error_response(message="Device Not Found")
    taskStrList = [task.getStatus() for task in current_app.config["device_map"][uuid].taskList]
    return success_response(data=taskStrList)
