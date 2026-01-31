"""统一响应格式"""
from flask import jsonify

class ApiResponse:
    """API响应封装"""
    
    @staticmethod
    def success(data=None, message="success", code=200):
        """成功响应"""
        response = {
            'code': code,
            'message': message,
            'data': data
        }
        return jsonify(response), code
    
    @staticmethod
    def error(message="error", code=400, data=None):
        """错误响应"""
        response = {
            'code': code,
            'message': message,
            'data': data
        }
        return jsonify(response), code
    
    @staticmethod
    def not_found(message="Resource not found"):
        """404响应"""
        return ApiResponse.error(message, 404)
    
    @staticmethod
    def validation_error(message="Validation failed"):
        """验证错误响应"""
        return ApiResponse.error(message, 400)
    
    @staticmethod
    def server_error(message="Internal server error"):
        """服务器错误响应"""
        return ApiResponse.error(message, 500)
