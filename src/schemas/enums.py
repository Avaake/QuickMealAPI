from enum import Enum


class OrderStatus(str, Enum):
    pending = "pending"
    preparing = "preparing"
    on_the_road = "on_the_road"
    delivered = "delivered"


class PaymentMethod(str, Enum):
    cash = "cash"
    online = "online"
    terminal = "terminal"
