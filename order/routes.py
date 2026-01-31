from flask import Blueprint, request, jsonify
from order.service import order_service
from order.model import Order
from common.exceptions import BusinessException
from common.response import ApiResponse
from common.logger import logger

order_bp = Blueprint('order', __name__)

@order_bp.route('/api/orders', methods=['GET'])
@order_bp.route('/order', methods=['GET'])
def list_all():
    """
    获取所有订单列表
    ---
    tags:
      - 订单管理
    responses:
      200:
        description: 成功返回订单列表
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: 订单ID
              orderSn:
                type: string
                description: 订单号
              productIds:
                type: array
                items:
                  type: integer
                description: 商品ID列表
              totalAmount:
                type: integer
                description: 总金额(分)
              createdAt:
                type: string
                format: date-time
                description: 创建时间
    """
    orders = order_service.list_all()
    return jsonify([o.to_dict() for o in orders])

@order_bp.route('/order/list', methods=['GET'])
@order_bp.route('/api/orders/list', methods=['GET'])
def list_orders():
    orders = order_service.list_all()
    return jsonify([o.to_dict() for o in orders])

@order_bp.route('/api/orders/<int:id>', methods=['GET'])
@order_bp.route('/order/<int:id>', methods=['GET'])
def get_by_id(id):
    """
    根据ID获取订单详情
    ---
    tags:
      - 订单管理
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: 订单ID
    responses:
      200:
        description: 成功返回订单详情
        schema:
          type: object
          properties:
            id:
              type: integer
            orderSn:
              type: string
            productIds:
              type: array
              items:
                type: integer
            totalAmount:
              type: integer
            createdAt:
              type: string
              format: date-time
      404:
        description: 订单不存在
    """
    order = order_service.find_by_id(id)
    if order:
        return jsonify(order.to_dict())
    return jsonify({'error': 'Order not found'}), 404

@order_bp.route('/api/orders', methods=['POST'])
@order_bp.route('/order', methods=['POST'])
def create():
    """
    创建新订单
    ---
    tags:
      - 订单管理
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - orderSn
            - productIds
            - totalAmount
          properties:
            orderSn:
              type: string
              description: 订单号
              example: "ORDER-TEST-001"
            productIds:
              type: array
              items:
                type: integer
              description: 商品ID列表
              example: [1, 2]
            totalAmount:
              type: integer
              description: 总金额(分)
              example: 49800
    responses:
      201:
        description: 订单创建成功
        schema:
          type: object
          properties:
            id:
              type: integer
            orderSn:
              type: string
            productIds:
              type: array
              items:
                type: integer
            totalAmount:
              type: integer
            createdAt:
              type: string
              format: date-time
      400:
        description: 请求参数错误
    """
    try:
        data = request.get_json()
        created = order_service.create(data)
        return jsonify(created.to_dict()), 201
    except BusinessException as e:
        logger.error(f"创建订单失败: {e.message}")
        return ApiResponse.error(e.message, e.code)

@order_bp.route('/api/orders/<int:id>', methods=['PUT'])
@order_bp.route('/order/<int:id>', methods=['PUT'])
def update(id):
    """
    更新订单信息
    ---
    tags:
      - 订单管理
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: 订单ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - orderSn
            - productIds
            - totalAmount
          properties:
            orderSn:
              type: string
              description: 订单号
            productIds:
              type: array
              items:
                type: integer
              description: 商品ID列表
            totalAmount:
              type: integer
              description: 总金额(分)
    responses:
      200:
        description: 订单更新成功
      404:
        description: 订单不存在
      400:
        description: 请求参数错误
    """
    try:
        data = request.get_json()
        result = order_service.update(id, data)
        return jsonify(result.to_dict())
    except BusinessException as e:
        logger.error(f"更新订单失败: {e.message}")
        return ApiResponse.error(e.message, e.code)

@order_bp.route('/api/orders/<int:id>', methods=['DELETE'])
@order_bp.route('/order/<int:id>', methods=['DELETE'])
def delete(id):
    """
    删除订单
    ---
    tags:
      - 订单管理
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: 订单ID
    responses:
      204:
        description: 订单删除成功
      404:
        description: 订单不存在
    """
    try:
        order_service.delete(id)
        return '', 204
    except BusinessException as e:
        logger.error(f"删除订单失败: {e.message}")
        return ApiResponse.error(e.message, e.code)
