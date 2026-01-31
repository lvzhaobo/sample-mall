from threading import Lock
from product.model import Product
import json
import os

class ProductRepository:
    def __init__(self):
        self.store = {}
        self.id_counter = 1
        self.lock = Lock()
        # 从JSON文件加载预置数据
        self._load_mock_data()
    
    def _load_mock_data(self):
        """从JSON文件加载Mock数据"""
        data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'products.json')
        if os.path.exists(data_file):
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    products_data = json.load(f)
                    for product_data in products_data:
                        self.save(Product(
                            None,
                            product_data['name'],
                            product_data['sku'],
                            product_data['stock'],
                            product_data['price']
                        ))
            except Exception as e:
                print(f"加载商品Mock数据失败: {e}")

    def find_all(self):
        return list(self.store.values())

    def find_by_id(self, product_id):
        return self.store.get(product_id)

    def save(self, product):
        with self.lock:
            if product.id is None:
                product.id = self.id_counter
                self.id_counter += 1
            self.store[product.id] = product
            return product

    def delete_by_id(self, product_id):
        with self.lock:
            if product_id in self.store:
                del self.store[product_id]
                return True
            return False

    def find_by_name_contains(self, keyword):
        if not keyword or not keyword.strip():
            return []
        keyword_lower = keyword.lower()
        return [p for p in self.store.values() 
                if p.name and keyword_lower in p.name.lower()]
    
    def find_by_sku(self, sku):
        """根据SKU查找商品"""
        if not sku:
            return None
        for product in self.store.values():
            if product.sku == sku:
                return product
        return None

# 全局实例
product_repository = ProductRepository()
