from order.repository import order_repository
from product.service import product_service
from common.exceptions import ResourceNotFoundException, DuplicateResourceException, ValidationException
from common.validators import OrderValidator
from common.logger import logger
from datetime import datetime

class OrderService:
    def __init__(self):
        self.repository = order_repository
        self.product_service = product_service

    def list_all(self):
        """获取所有订单"""
        logger.info("获取所有订单列表")
        return self.repository.find_all()

    def find_by_id(self, order_id):
        """根据ID查询订单"""
        logger.info(f"查询订单: id={order_id}")
        order = self.repository.find_by_id(order_id)
        if not order:
            logger.warning(f"订单不存在: id={order_id}")
            raise ResourceNotFoundException("Order", order_id)
        return order

    def create(self, order_data):
        """创建订单"""
        logger.info(f"创建订单: {order_data}")
        
        # 数据验证
        OrderValidator.validate_create(order_data)
        
        # 检查订单号是否重复
        order_sn = order_data.get('orderSn')
        if self.repository.find_by_order_sn(order_sn):
            logger.warning(f"订单号已存在: {order_sn}")
            raise DuplicateResourceException(f"订单号已存在: {order_sn}")
        
        # 验证商品是否存在并计算总金额
        product_ids = order_data.get('productIds', [])
        total_amount = 0
        for product_id in product_ids:
            try:
                product = self.product_service.find_by_id(product_id)
                total_amount += product.price
            except ResourceNotFoundException:
                logger.warning(f"订单包含不存在的商品: product_id={product_id}")
                raise ValidationException(f"商品不存在: {product_id}")
        
        # 自动计算总金额（如果未提供或不匹配）
        if order_data.get('totalAmount') is None:
            order_data['totalAmount'] = total_amount
        
        from order.model import Order
        order = Order.from_dict(order_data)
        order.created_at = datetime.now()
        
        created = self.repository.save(order)
        logger.info(f"订单创建成功: id={created.id}, orderSn={created.order_sn}")
        return created

    def update(self, order_id, updated_data):
        """更新订单"""
        logger.info(f"更新订单: id={order_id}, data={updated_data}")
        
        # 数据验证
        OrderValidator.validate_update(updated_data)
        
        existing = self.repository.find_by_id(order_id)
        if not existing:
            logger.warning(f"订单不存在: id={order_id}")
            raise ResourceNotFoundException("Order", order_id)
        
        # 检查订单号是否与其他订单重复
        new_order_sn = updated_data.get('orderSn')
        if new_order_sn != existing.order_sn:
            sn_order = self.repository.find_by_order_sn(new_order_sn)
            if sn_order and sn_order.id != order_id:
                logger.warning(f"订单号已被其他订单使用: {new_order_sn}")
                raise DuplicateResourceException(f"订单号已被其他订单使用: {new_order_sn}")
        
        # 验证商品是否存在
        product_ids = updated_data.get('productIds', [])
        for product_id in product_ids:
            try:
                self.product_service.find_by_id(product_id)
            except ResourceNotFoundException:
                logger.warning(f"订单包含不存在的商品: product_id={product_id}")
                raise ValidationException(f"商品不存在: {product_id}")
        
        existing.order_sn = updated_data.get('orderSn')
        existing.product_ids = updated_data.get('productIds')
        existing.total_amount = updated_data.get('totalAmount')
        
        updated = self.repository.save(existing)
        logger.info(f"订单更新成功: id={order_id}")
        return updated

    def delete(self, order_id):
        """删除订单"""
        logger.info(f"删除订单: id={order_id}")
        
        if not self.repository.find_by_id(order_id):
            logger.warning(f"订单不存在: id={order_id}")
            raise ResourceNotFoundException("Order", order_id)
        
        success = self.repository.delete_by_id(order_id)
        logger.info(f"订单删除成功: id={order_id}")
        return success
    
    def find_by_order_sn(self, order_sn):
        """根据订单号查询订单"""
        logger.info(f"根据订单号查询: orderSn={order_sn}")
        return self.repository.find_by_order_sn(order_sn)

# 全局实例
order_service = OrderService()
