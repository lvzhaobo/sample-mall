# sample-mall

轻量级商城后端服务 - Python Flask 版本 

## 项目特性

### 📦 核心功能
- ✅ 商品管理 (CRUD + 搜索)
- ✅ 订单管理 (CRUD + 业务逻辑)
- ✅ 内存存储 (无需数据库)
- ✅ RESTful API

### 🛠 技术亮点
- **异常处理体系**: 自定义业务异常,统一错误响应
- **数据验证**: 完善的输入验证器
- **日志系统**: 结构化日志记录
- **配置管理**: 多环境配置支持
- **代码结构**: 清晰的三层架构 (Controller/Service/Repository)

### 🎯 代码质量
- 完整的异常处理机制
- 业务逻辑验证 (SKU重复检查、订单号唯一性等)
- 库存管理功能
- 自动计算订单总金额
- 健康检查接口

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动应用
```bash
# Windows
.\run.ps1

# Linux/Mac
chmod +x run.sh
./run.sh

# 或直接运行
python app.py
```

### 3. 访问服务
- 应用地址: http://localhost:8080
- 健康检查: http://localhost:8080/health

## API 接口

### 商品管理
```bash
# 获取所有商品
GET /api/products

# 搜索商品
GET /product/list?keyword=示例

# 获取单个商品
GET /api/products/1

# 创建商品
POST /api/products
{
  "name": "测试商品",
  "sku": "SKU-TEST",
  "stock": 100,
  "price": 9900
}

# 更新商品
PUT /api/products/1
{
  "name": "更新商品",
  "sku": "SKU-UPDATE",
  "stock": 200,
  "price": 19900
}

# 删除商品
DELETE /api/products/1
```

### 订单管理
```bash
# 获取所有订单
GET /api/orders

# 获取单个订单
GET /api/orders/1

# 创建订单
POST /api/orders
{
  "orderSn": "ORDER-TEST-001",
  "productIds": [1, 2],
  "totalAmount": 29800
}

# 更新订单
PUT /api/orders/1
{
  "orderSn": "ORDER-UPDATE-001",
  "productIds": [1],
  "totalAmount": 19900
}

# 删除订单
DELETE /api/orders/1
```

## 项目结构

```
sample-mall/
├── app.py                  # 应用入口与工厂函数
├── config.py               # 配置管理
├── requirements.txt        # 依赖列表
├── common/                 # 公共模块
│   ├── exceptions.py       # 自定义异常
│   ├── response.py         # 统一响应格式
│   ├── validators.py       # 数据验证器
│   └── logger.py           # 日志配置
├── product/                # 商品模块
│   ├── model.py           # 数据模型
│   ├── repository.py      # 数据访问层
│   ├── service.py         # 业务逻辑层
│   └── routes.py          # 路由控制层
└── order/                  # 订单模块
    ├── model.py           # 数据模型
    ├── repository.py      # 数据访问层
    ├── service.py         # 业务逻辑层
    └── routes.py          # 路由控制层
```

## 技术栈

- **Web框架**: Flask 3.0
- **CORS支持**: flask-cors
- **数据存储**: 内存字典 + 线程锁
- **日志**: Python logging
- **配置**: 环境变量 + 配置类

## 业务特性

### 数据验证
- 商品名称、SKU、价格、库存验证
- 订单号、商品列表、总金额验证
- 字段长度限制
- 数据类型检查

### 业务规则
- SKU唯一性检查
- 订单号唯一性检查
- 商品存在性验证
- 库存管理 (减库存功能)
- 订单总金额自动计算

### 异常处理
- 资源未找到异常
- 数据验证异常
- 资源重复异常
- 库存不足异常
- 全局异常拦截器

## 环境配置

复制 `.env.example` 为 `.env` 并修改配置:

```bash
# 开发环境
FLASK_ENV=development
FLASK_DEBUG=True

# 生产环境
FLASK_ENV=production
FLASK_DEBUG=False
```

