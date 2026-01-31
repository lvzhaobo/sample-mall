class Product:
    def __init__(self, id=None, name=None, sku=None, stock=None, price=None):
        self.id = id
        self.name = name
        self.sku = sku
        self.stock = stock
        self.price = price  # 单位：分

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'sku': self.sku,
            'stock': self.stock,
            'price': self.price
        }

    @staticmethod
    def from_dict(data):
        return Product(
            id=data.get('id'),
            name=data.get('name'),
            sku=data.get('sku'),
            stock=data.get('stock'),
            price=data.get('price')
        )
