# 今天是否值得买入
TODAY_IS_BUY = True
# 目标价格
TARGET_PRICE = 0.5

# 买入订单
BUY_ORDERS = []
# 卖出订单
SELL_ORDERS = []


class Order:
    def __init__(self, order_id, order_price, order_status):
        self.order_id = order_id
        self.order_price = order_price
        self.order_status = order_status
