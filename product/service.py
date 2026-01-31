from product.repository import product_repository
from product.model import Product
from common.exceptions import ResourceNotFoundException, DuplicateResourceException, ValidationException
from common.validators import ProductValidator
from common.logger import logger

class ProductService:
    def __init__(self):
        self.repository = product_repository

    def list_all(self):
        """获取所有商品"""
        logger.info("获取所有商品列表")
        return self.repository.find_all()

    def find_by_id(self, product_id):
        """根据ID查询商品"""
        logger.info(f"查询商品: id={product_id}")
        product = self.repository.find_by_id(product_id)
        if not product:
            logger.warning(f"商品不存在: id={product_id}")
            raise ResourceNotFoundException("Product", product_id)
        return product

    def create(self, product_data):
        """创建商品"""
        logger.info(f"创建商品: {product_data}")
        
        # 数据验证
        ProductValidator.validate_create(product_data)
        
        # 检查SKU是否重复
        sku = product_data.get('sku')
        if self.repository.find_by_sku(sku):
            logger.warning(f"SKU已存在: {sku}")
            raise DuplicateResourceException(f"商品SKU已存在: {sku}")
        
        product = Product.from_dict(product_data)
        created = self.repository.save(product)
        logger.info(f"商品创建成功: id={created.id}")
        return created

    def update(self, product_id, updated_data):
        """更新商品"""
        logger.info(f"更新商品: id={product_id}, data={updated_data}")
        
        # 数据验证
        ProductValidator.validate_update(updated_data)
        
        existing = self.repository.find_by_id(product_id)
        if not existing:
            logger.warning(f"商品不存在: id={product_id}")
            raise ResourceNotFoundException("Product", product_id)
        
        # 检查SKU是否与其他商品重复
        new_sku = updated_data.get('sku')
        if new_sku != existing.sku:
            sku_product = self.repository.find_by_sku(new_sku)
            if sku_product and sku_product.id != product_id:
                logger.warning(f"SKU已被其他商品使用: {new_sku}")
                raise DuplicateResourceException(f"商品SKU已被其他商品使用: {new_sku}")
        
        existing.name = updated_data.get('name')
        existing.sku = updated_data.get('sku')
        existing.stock = updated_data.get('stock')
        existing.price = updated_data.get('price')
        
        updated = self.repository.save(existing)
        logger.info(f"商品更新成功: id={product_id}")
        return updated

    def delete(self, product_id):
        """删除商品"""
        logger.info(f"删除商品: id={product_id}")
        
        if not self.repository.find_by_id(product_id):
            logger.warning(f"商品不存在: id={product_id}")
            raise ResourceNotFoundException("Product", product_id)
        
        success = self.repository.delete_by_id(product_id)
        logger.info(f"商品删除成功: id={product_id}")
        return success

    def search_by_name(self, keyword):
        """按名称搜索商品"""
        logger.info(f"搜索商品: keyword={keyword}")
        return self.repository.find_by_name_contains(keyword)
    
    def reduce_stock(self, product_id, quantity):
        """减少库存"""
        logger.info(f"减少库存: product_id={product_id}, quantity={quantity}")
        
        product = self.find_by_id(product_id)
        if product.stock < quantity:
            from common.exceptions import InsufficientStockException
            raise InsufficientStockException(product_id, quantity, product.stock)
        
        product.stock -= quantity
        return self.repository.save(product)

# 全局实例
product_service = ProductService()
