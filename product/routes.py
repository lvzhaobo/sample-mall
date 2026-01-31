from flask import Blueprint, request, jsonify
from product.service import product_service
from product.model import Product
from common.exceptions import BusinessException
from common.response import ApiResponse
from common.logger import logger

product_bp = Blueprint('product', __name__)

@product_bp.route('/api/products', methods=['GET'])
@product_bp.route('/product', methods=['GET'])
def list_all():
    """
    获取所有商品列表
    ---
    tags:
      - 商品管理
    responses:
      200:
        description: 成功返回商品列表
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: 商品ID
              name:
                type: string
                description: 商品名称
              sku:
                type: string
                description: 商品SKU
              stock:
                type: integer
                description: 库存数量
              price:
                type: integer
                description: 价格(分)
    """
    products = product_service.list_all()
    return jsonify([p.to_dict() for p in products])

@product_bp.route('/product/list', methods=['GET'])
@product_bp.route('/api/products/list', methods=['GET'])
def list_products():
    """
    查询商品列表(支持关键词搜索)
    ---
    tags:
      - 商品管理
    parameters:
      - name: keyword
        in: query
        type: string
        required: false
        description: 搜索关键词
    responses:
      200:
        description: 成功返回商品列表
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              sku:
                type: string
              stock:
                type: integer
              price:
                type: integer
    """
    keyword = request.args.get('keyword')
    if keyword:
        products = product_service.search_by_name(keyword)
    else:
        products = product_service.list_all()
    return jsonify([p.to_dict() for p in products])

@product_bp.route('/api/products/<int:id>', methods=['GET'])
@product_bp.route('/product/<int:id>', methods=['GET'])
def get_by_id(id):
    """
    根据ID获取商品详情
    ---
    tags:
      - 商品管理
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: 商品ID
    responses:
      200:
        description: 成功返回商品详情
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            sku:
              type: string
            stock:
              type: integer
            price:
              type: integer
      404:
        description: 商品不存在
    """
    product = product_service.find_by_id(id)
    if product:
        return jsonify(product.to_dict())
    return jsonify({'error': 'Product not found'}), 404

@product_bp.route('/api/products', methods=['POST'])
@product_bp.route('/product', methods=['POST'])
def create():
    """
    创建新商品
    ---
    tags:
      - 商品管理
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - sku
            - stock
            - price
          properties:
            name:
              type: string
              description: 商品名称
              example: "测试商品"
            sku:
              type: string
              description: 商品SKU
              example: "SKU-TEST-001"
            stock:
              type: integer
              description: 库存数量
              example: 100
            price:
              type: integer
              description: 价格(分)
              example: 9900
    responses:
      201:
        description: 商品创建成功
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            sku:
              type: string
            stock:
              type: integer
            price:
              type: integer
      400:
        description: 请求参数错误
    """
    try:
        data = request.get_json()
        created = product_service.create(data)
        return jsonify(created.to_dict()), 201
    except BusinessException as e:
        logger.error(f"创建商品失败: {e.message}")
        return ApiResponse.error(e.message, e.code)

@product_bp.route('/api/products/<int:id>', methods=['PUT'])
@product_bp.route('/product/<int:id>', methods=['PUT'])
def update(id):
    """
    更新商品信息
    ---
    tags:
      - 商品管理
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: 商品ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - sku
            - stock
            - price
          properties:
            name:
              type: string
              description: 商品名称
            sku:
              type: string
              description: 商品SKU
            stock:
              type: integer
              description: 库存数量
            price:
              type: integer
              description: 价格(分)
    responses:
      200:
        description: 商品更新成功
      404:
        description: 商品不存在
      400:
        description: 请求参数错误
    """
    try:
        data = request.get_json()
        result = product_service.update(id, data)
        return jsonify(result.to_dict())
    except BusinessException as e:
        logger.error(f"更新商品失败: {e.message}")
        return ApiResponse.error(e.message, e.code)

@product_bp.route('/api/products/<int:id>', methods=['DELETE'])
@product_bp.route('/product/<int:id>', methods=['DELETE'])
def delete(id):
    """
    删除商品
    ---
    tags:
      - 商品管理
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: 商品ID
    responses:
      204:
        description: 商品删除成功
      404:
        description: 商品不存在
    """
    try:
        product_service.delete(id)
        return '', 204
    except BusinessException as e:
        logger.error(f"删除商品失败: {e.message}")
        return ApiResponse.error(e.message, e.code)

@product_bp.route('/product/simpleList', methods=['GET'])
@product_bp.route('/api/products/simpleList', methods=['GET'])
def simple_list():
    keyword = request.args.get('keyword')
    products = product_service.search_by_name(keyword) if keyword else []
    return jsonify([p.to_dict() for p in products])

@product_bp.route('/product/search', methods=['GET'])
@product_bp.route('/api/products/search', methods=['GET'])
def search():
    keyword = request.args.get('q')
    products = product_service.search_by_name(keyword) if keyword else []
    return jsonify([p.to_dict() for p in products])
