# 用于控制设备连接类请请求处理
from flask import Blueprint, request, current_app

from src.app import SCREENSHOT_METHODS, TOUCH_METHODS
from src.app.Models.ResponseResult import success_response, error_response
from src.app.Service import DeviceService

deviceController = Blueprint('deviceController', __name__)


@deviceController.route('/getAdbDeviceList')
def getAdbDeviceList():
    return DeviceService.getAdbDeviceList()


@deviceController.route('/getScreenshotMethods')
def getScreenshotMethods():
    return success_response(data=SCREENSHOT_METHODS)


@deviceController.route('/getTouchMethods')
def getTouchMethods():
    return success_response(data=TOUCH_METHODS)


@deviceController.route('/connectAdbDeviceRemote', methods=['POST'])
def connectAdbDeviceRemote():
    data = request.json
    address = data['address']
    return DeviceService.connectAdbDeviceRemote(address)


@deviceController.route('/disconnectAdbDeviceRemote', methods=['POST'])
def disconnectAdbDeviceRemote():
    data = request.json
    address = data['address']
    return DeviceService.disconnectAdbDeviceRemote(address)


@deviceController.route('/connectDevice', methods=['POST'])
def connectDevice():
    data = request.json  # 获取数据
    device, uuid, result = DeviceService.connectDevice(data)  # 连接设备逻辑
    if device and uuid:
        current_app.config["device_map"][uuid] = device  # 设备实例存储在deviceList中
    return result


@deviceController.route('/disconnectDevice', methods=['POST'])
def disconnectDevice():
    data = request.json
    uuid = data['uuid']
    if uuid in current_app.config["device_map"]:
        del current_app.config["device_map"][uuid]
        return success_response(message="Disconnected")
    return error_response(message="Not connected")


@deviceController.route('/getDeviceList')
def getDeviceList():
    return success_response(data=[key for (key, _) in current_app.config["device_map"].items()])
