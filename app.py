import os
from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from product.routes import product_bp
from order.routes import order_bp
from config import config
from common.logger import logger
from common.exceptions import BusinessException

def create_app(config_name=None):
    """应用工厂函数"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))
    
    # 配置CORS
    CORS(app, resources={r"/*": {"origins": app.config['CORS_ORIGINS']}})
    
    # 配置Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api-docs/"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Sample Mall API",
            "description": "轻量级商城后端服务 API 文档 (Python Flask版本)",
            "version": "1.0.0",
            "contact": {
                "name": "Sample Mall Team"
            }
        },
        "host": "localhost:8080",
        "basePath": "/",
        "schemes": ["http"],
        "tags": [
            {
                "name": "商品管理",
                "description": "商品相关的增删改查操作"
            },
            {
                "name": "订单管理",
                "description": "订单相关的增删改查操作"
            }
        ]
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # 注册蓝图
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)
    
    # 注册全局异常处理器
    @app.errorhandler(BusinessException)
    def handle_business_exception(e):
        logger.error(f"业务异常: {e.message}")
        return jsonify({
            'code': e.code,
            'message': e.message,
            'data': None
        }), e.code
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            'code': 404,
            'message': 'Resource not found',
            'data': None
        }), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        logger.error(f"服务器错误: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'Internal server error',
            'data': None
        }), 500
    
    @app.route('/')
    def index():
        return {
            'name': 'sample-mall',
            'description': '轻量级商城后端服务 (Python Flask版本)',
            'version': '1.0.0',
            'environment': config_name
        }
    
    @app.route('/admin')
    def admin():
        """前端管理页面"""
        from flask import send_from_directory
        return send_from_directory('static', 'index.html')
    
    @app.route('/health')
    def health():
        """健康检查接口"""
        return {'status': 'healthy', 'service': 'sample-mall'}
    
    logger.info(f"应用启动: 环境={config_name}")
    return app

app = create_app()

if __name__ == '__main__':
    from config import Config
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
