import json
import datetime
from .email import send_email
from .hk import get_xiaomi_news, get_xiaomi_dashi, get_all_hk_trend, get_xiaomi_rating, submit_order, sell_order
from .query import client, model
from .constans import system_prompt, get_question_prompt
from .order import SELL_ORDERS, TODAY_IS_BUY


class BaseMonitor:
    def __init__(self, name):
        self.name = name
        self.time = "00:00"

    def start(self):
        print(f"========>【{self.name}】任务开始执行<========")
        try:
            content = self.run()
            send_email(self.name, content)
        except Exception as e:
            print(f"========>【{self.name}】任务执行失败<========")
            print(e)
        print(f"========>【{self.name}】任务执行结束<========")

    def run(self):
        pass


class OpeningMonitor(BaseMonitor):
    def __init__(self, name):
        super().__init__(name)
        self.time = "09:00"

    def run(self):
        """
        开盘前准备工作:
        1. 获取小米最近大事件
        2. 获取小米最近新闻
        """
        xiaomi_dashi = get_xiaomi_dashi()
        xiaomi_news = get_xiaomi_news()
        xiaomi_rating = get_xiaomi_rating()
        response = client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "当前时间多久?"},
                {"role": "assistant", "content": "当前时间为北京时间：" +
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ", 距离今日开盘时间还剩30分钟"},
                {"role": "user", "content": "小米最近有什么大事件? 用JSON格式返回"},
                {"role": "assistant", "content": json.dumps(xiaomi_dashi)},
                {"role": "user", "content": "小米最近有什么新闻? 用JSON格式返回"},
                {"role": "assistant", "content": json.dumps(xiaomi_news)},
                {"role": "user", "content": "小米最近投资评级? 用JSON格式返回"},
                {"role": "assistant", "content": json.dumps(xiaomi_rating)},
                {"role": "user", "content": get_question_prompt("Xiaomi stock opening today")},
            ],
        )
        content = json.loads(response.choices[0].message.content)
        global TODAY_IS_BUY
        TODAY_IS_BUY = content["isCanBuy"]
        return content['reason']


class StockMonitor(BaseMonitor):
    def __init__(self, name):
        super().__init__(name)
        self.time = "09:40"

    def run(self):
        """
        港股整体趋势
        """
        # 如果昨天买入的订单, 今天还没有卖出, 则不买入
        if len(SELL_ORDERS) > 0:
            return "昨天的订单还没有卖出, 今天不能买入小米"

        # 获取港股整体趋势, 判断是否值得买入
        hk_trend = get_all_hk_trend()
        response = client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "当前时间多久?"},
                {"role": "assistant", "content": "当前时间为北京时间：" +
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ", 距离今日开盘时间已经过去10分钟"},
                {"role": "user", "content": "今天港股整体数据实时情况是什么?"},
                {"role": "assistant", "content": "港股数据：" +
                    json.dumps(hk_trend)},
                {"role": "user", "content": get_question_prompt(
                    "Overall situation of Hong Kong stocks, is it suitable to buy Xiaomi?")},
            ],
        )
        content = json.loads(response.choices[0].message.content)
        print(content)
        global TODAY_IS_BUY
        TODAY_IS_BUY = content["isCanBuy"]
        # 如果今天值得买入, 则下单
        if TODAY_IS_BUY:
            print("开始下单")
            order_id = submit_order()
            return "下单成功, 订单ID: " + order_id
        else:
            return content['reason']


class TradeMonitor(BaseMonitor):
    def __init__(self, name):
        super().__init__(name)
        self.time = "09:45"

    def run(self):
        sell_order()
        return "收盘"
