import schedule
import time
from datetime import datetime
from core import OpeningMonitor, StockMonitor, TradeMonitor
from core.hk import submit_order


"""
交易策略：
1. 只做短线，每天只做一次交易
2. 每天开盘前，判断昨天的订单是否存在，存在则不买入
3. 每天开盘前进行股市分析，判断是否买入小米
4. 开盘后10分钟开始买入
5. 买入后，查询订单详情，订单如果买入成功，则开始监听价格变动，如果价格超过5个点，则卖出。如果一直下跌，则一直持有。
6. 按照最大购买力，每天稳定收入1800*x.50-1800*x-200=700元， 一年就是250 * 700 = 175000元，最大购买力会随着收益增加而增加，差不多一年20万。
"""
monitor = [
    # 盘前分析
    OpeningMonitor("开盘前分析"),
    # 买入小米
    # StockMonitor("开盘后10分钟，整体港股趋势"),
    # 卖出小米
    # TradeMonitor("卖出小米")
]
for m in monitor:
    schedule.every().day.at(m.time).do(m.start)

print("服务启动成功，现在是北京时间：", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

while True:
    schedule.run_pending()
    time.sleep(1)