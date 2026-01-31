"""数据验证工具"""
from common.exceptions import ValidationException
from config import Config

class ProductValidator:
    """商品数据验证器"""
    
    @staticmethod
    def validate_create(data):
        """验证创建商品的数据"""
        if not data:
            raise ValidationException("请求数据不能为空")
        
        # 验证商品名称
        name = data.get('name')
        if not name or not name.strip():
            raise ValidationException("商品名称不能为空")
        if len(name) > 200:
            raise ValidationException("商品名称长度不能超过200个字符")
        
        # 验证SKU
        sku = data.get('sku')
        if not sku or not sku.strip():
            raise ValidationException("商品SKU不能为空")
        if len(sku) > 100:
            raise ValidationException("商品SKU长度不能超过100个字符")
        
        # 验证库存
        stock = data.get('stock')
        if stock is None:
            raise ValidationException("商品库存不能为空")
        if not isinstance(stock, int) or stock < 0:
            raise ValidationException("商品库存必须是非负整数")
        if stock > Config.MAX_PRODUCT_STOCK:
            raise ValidationException(f"商品库存不能超过{Config.MAX_PRODUCT_STOCK}")
        
        # 验证价格
        price = data.get('price')
        if price is None:
            raise ValidationException("商品价格不能为空")
        if not isinstance(price, int) or price < Config.MIN_PRODUCT_PRICE:
            raise ValidationException(f"商品价格必须大于等于{Config.MIN_PRODUCT_PRICE}分")
        if price > Config.MAX_PRODUCT_PRICE:
            raise ValidationException(f"商品价格不能超过{Config.MAX_PRODUCT_PRICE}分")
    
    @staticmethod
    def validate_update(data):
        """验证更新商品的数据"""
        ProductValidator.validate_create(data)

class OrderValidator:
    """订单数据验证器"""
    
    @staticmethod
    def validate_create(data):
        """验证创建订单的数据"""
        if not data:
            raise ValidationException("请求数据不能为空")
        
        # 验证订单号
        order_sn = data.get('orderSn')
        if not order_sn or not order_sn.strip():
            raise ValidationException("订单号不能为空")
        if len(order_sn) > 100:
            raise ValidationException("订单号长度不能超过100个字符")
        
        # 验证商品ID列表
        product_ids = data.get('productIds')
        if not product_ids:
            raise ValidationException("订单商品列表不能为空")
        if not isinstance(product_ids, list):
            raise ValidationException("商品ID列表格式错误")
        if len(product_ids) > Config.MAX_PRODUCTS_PER_ORDER:
            raise ValidationException(f"单个订单商品数量不能超过{Config.MAX_PRODUCTS_PER_ORDER}")
        
        # 验证商品ID类型
        for pid in product_ids:
            if not isinstance(pid, int) or pid <= 0:
                raise ValidationException("商品ID必须是正整数")
        
        # 验证总金额
        total_amount = data.get('totalAmount')
        if total_amount is None:
            raise ValidationException("订单总金额不能为空")
        if not isinstance(total_amount, int) or total_amount < 0:
            raise ValidationException("订单总金额必须是非负整数")
    
    @staticmethod
    def validate_update(data):
        """验证更新订单的数据"""
        OrderValidator.validate_create(data)
