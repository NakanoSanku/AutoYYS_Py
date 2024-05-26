from flask import Flask
from flask_cors import CORS
from src.app.Controller.DeviceController import deviceController
from src.app.Controller.TaskController import taskController
app = Flask(__name__)
CORS(app)  # 解决跨域请求失败问题
app.register_blueprint(deviceController, url_prefix='/device')
app.register_blueprint(taskController, url_prefix='/task')

# 创建设备实例Map 共享给Controller使用current_app["device_map"]使用
device_map = {}
app.config['device_map'] = device_map

if __name__ == '__main__':
    app.run(debug=True)
