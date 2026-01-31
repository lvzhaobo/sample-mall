from threading import Lock
from datetime import datetime
from order.model import Order
import json
import os

class OrderRepository:
    def __init__(self):
        self.store = {}
        self.id_counter = 1
        self.lock = Lock()
        # 从JSON文件加载预置数据
        self._load_mock_data()
    
    def _load_mock_data(self):
        """从JSON文件加载Mock数据"""
        data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'orders.json')
        if os.path.exists(data_file):
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    orders_data = json.load(f)
                    for order_data in orders_data:
                        self.save(Order(
                            None,
                            order_data['orderSn'],
                            order_data['productIds'],
                            order_data['totalAmount'],
                            datetime.now()
                        ))
            except Exception as e:
                print(f"加载订单Mock数据失败: {e}")

    def find_all(self):
        return list(self.store.values())

    def find_by_id(self, order_id):
        return self.store.get(order_id)

    def save(self, order):
        with self.lock:
            if order.id is None:
                order.id = self.id_counter
                self.id_counter += 1
            if order.created_at is None:
                order.created_at = datetime.now()
            self.store[order.id] = order
            return order

    def delete_by_id(self, order_id):
        with self.lock:
            if order_id in self.store:
                del self.store[order_id]
                return True
            return False
    
    def find_by_order_sn(self, order_sn):
        """根据订单号查找订单"""
        if not order_sn:
            return None
        for order in self.store.values():
            if order.order_sn == order_sn:
                return order
        return None

# 全局实例
order_repository = OrderRepository()
