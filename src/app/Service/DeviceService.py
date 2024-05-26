import subprocess
import uuid

from adbutils import adb, AdbError, AdbTimeout, AdbClient, adb_path
from marshmallow import Schema, fields, ValidationError, validates_schema
from marshmallow.validate import OneOf
from pygamescript import GameScript

from src.app.Models.Device import Device
from src.app.Models.ResponseResult import success_response, error_response
from src.app import SCREENSHOT_METHODS, TOUCH_METHODS, TOUCH_METHODS_MAP, SCREENSHOT_METHODS_MAP


class ConnectDeviceSchema(Schema):
    serial = fields.Str(required=False)
    screenshotMethod = fields.Str(required=True, validate=OneOf(SCREENSHOT_METHODS))
    touchMethod = fields.Str(required=True, validate=OneOf(TOUCH_METHODS))
    handle = fields.Str(required=False)
    instanceIndex = fields.Int(required=False)
    emulatorInstallPath = fields.Str(required=False)
    debug = fields.Bool(required=False, missing=False)

    @validates_schema
    def validate_methods(self, data, **kwargs):
        screenshot_method = data.get('screenshotMethod')
        touch_method = data.get('touchMethod')
        handle = data.get('handle')
        instance_index = data.get('instanceIndex')
        emulator_install_path = data.get('emulatorInstallPath')
        serial = data.get('serial')

        errors = {}

        if (touch_method == "windows" or screenshot_method == "windows") and not handle:
            errors['handle'] = ["Handle is required for windows methods"]

        if screenshot_method == "MuMu" or touch_method == "MuMu":
            if instance_index is None:
                errors['instanceIndex'] = ["Instance index is required for MuMu methods"]
            if not emulator_install_path:
                errors['emulatorInstallPath'] = ["Emulator install path is required for MuMu methods"]

        if (screenshot_method not in ["windows", "MuMu"] or touch_method not in ["windows", "MuMu"]) and not serial:
            errors['serial'] = ["Serial is required for ADB methods"]

        if errors:
            raise ValidationError(errors)


def getAdbDeviceList():
    try:
        devices = [device.serial for device in adb.device_list()]
    except AdbTimeout as e:
        adb.server_kill()
        subprocess.run([adb_path(), "devices"])  # 如果存在设备且仅存在一台并且该设备状态为 offline时adbutils无法直接使用,需手动adb devices
        return error_response(message="设备连接失败,重启ADB,请稍后重试\nlog:{}".format(e))
    if len(devices) == 0:
        return error_response(message="没有连接的ADB设备")
    return success_response(data=devices)


def connectAdbDeviceRemote(address: str):
    try:
        msg = adb.connect(address)
    except AdbTimeout as e:
        return error_response(message="连接超时哩\nlog:{}".format(e))
    if "fail" or "cannot" in msg:
        return error_response(message=msg)
    return success_response(message=msg)


def disconnectAdbDeviceRemote(address):
    try:
        msg = adb.disconnect(address, raise_error=True)
    except AdbError as e:
        return error_response(message="不存在该设备捏\nlog:{}".format(e))
    return success_response(message=msg)


def connectDevice(data):
    # 使用验证类验证数据
    schema = ConnectDeviceSchema()
    try:
        schemaData = schema.load(data)
    except ValidationError as err:
        return None, None, error_response(message=err.messages)

    serial = schemaData.get('serial')
    screenshot_method = schemaData.get('screenshotMethod')
    touch_method = schemaData.get('touchMethod')
    handle = schemaData.get('handle')
    instance_index = schemaData.get('instanceIndex')
    emulator_install_path = schemaData.get('emulatorInstallPath')
    debug = schemaData.get('debug')

    try:
        touch_method_ex = TOUCH_METHODS_MAP[touch_method]
        screenshot_method_ex = SCREENSHOT_METHODS_MAP[screenshot_method]

        touch_method_ex = touch_method_ex(handle) if touch_method == 'windows' else \
            touch_method_ex(instance_index, emulator_install_path) if touch_method == 'MuMu' else \
                touch_method_ex(serial)

        screenshot_method_ex = screenshot_method_ex(handle) if screenshot_method == 'windows' else \
            screenshot_method_ex(instance_index, emulator_install_path) if screenshot_method == 'MuMu' else \
                screenshot_method_ex(serial)

        tmp_device = GameScript(capMethod=screenshot_method_ex, touchMethod=touch_method_ex, debug=debug)
        tmp_device.screenshot()
        tmp_device.click(1, 1)
    except Exception as e:
        return None, None, error_response(message="{}".format(e))
    deviceUUID = str(uuid.uuid4())

    return Device(device=tmp_device), deviceUUID, success_response(data=deviceUUID)
