from enum import Enum


class OrderStatus(str, Enum):
    pending = "pending"
    preparing = "preparing"
    on_the_road = "on_the_road"
    delivered = "delivered"


class PaymentMethod(str, Enum):
    online = "online"
    terminal = "terminal"
    cash = "cash"
