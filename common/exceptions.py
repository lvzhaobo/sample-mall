"""自定义异常类"""

class BusinessException(Exception):
    """业务异常基类"""
    def __init__(self, message, code=400):
        self.message = message
        self.code = code
        super().__init__(self.message)

class ResourceNotFoundException(BusinessException):
    """资源未找到异常"""
    def __init__(self, resource_type, resource_id):
        message = f"{resource_type} not found: {resource_id}"
        super().__init__(message, code=404)

class ValidationException(BusinessException):
    """数据验证异常"""
    def __init__(self, message):
        super().__init__(message, code=400)

class InsufficientStockException(BusinessException):
    """库存不足异常"""
    def __init__(self, product_id, required, available):
        message = f"商品 {product_id} 库存不足: 需要 {required}, 可用 {available}"
        super().__init__(message, code=400)

class DuplicateResourceException(BusinessException):
    """资源重复异常"""
    def __init__(self, message):
        super().__init__(message, code=409)
