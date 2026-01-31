import os

class Config:
    """应用配置类"""
    
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Flask配置
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FLASK_PORT', 8080))
    
    # CORS配置
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    
    # 业务配置
    MAX_PRODUCTS_PER_ORDER = 100
    MIN_PRODUCT_PRICE = 1  # 最低价格1分
    MAX_PRODUCT_PRICE = 999999900  # 最高价格
    MAX_PRODUCT_STOCK = 999999
    
    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False

class TestConfig(Config):
    """测试环境配置"""
    TESTING = True

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig,
    'default': DevelopmentConfig
}
