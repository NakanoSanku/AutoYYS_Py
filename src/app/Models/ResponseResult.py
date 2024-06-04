# 用于生成API响应结果
from flask import jsonify


class ResponseResult:
    def __init__(self, code=200, message="Success", data=None):
        self.code = code
        self.message = message
        self.data = data

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
            "data": self.data
        }


def success_response(data=None, message="Success"):
    result = ResponseResult(code=200, message=message, data=data)
    return jsonify(result.to_dict()), 200


def error_response(message="Error"):
    response = jsonify({
        "error": "Bad Request",
        "message": message
    })
    response.status_code = 400
    return response


