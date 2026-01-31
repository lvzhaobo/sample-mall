from datetime import datetime

class Order:
    def __init__(self, id=None, order_sn=None, product_ids=None, total_amount=None, created_at=None):
        self.id = id
        self.order_sn = order_sn
        self.product_ids = product_ids or []
        self.total_amount = total_amount
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'orderSn': self.order_sn,
            'productIds': self.product_ids,
            'totalAmount': self.total_amount,
            'createdAt': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }

    @staticmethod
    def from_dict(data):
        created_at = data.get('createdAt')
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at)
            except:
                created_at = datetime.now()
        
        return Order(
            id=data.get('id'),
            order_sn=data.get('orderSn'),
            product_ids=data.get('productIds', []),
            total_amount=data.get('totalAmount'),
            created_at=created_at
        )
