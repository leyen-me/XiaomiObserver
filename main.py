import schedule
import time
from datetime import datetime
from core import OpeningMonitor

monitor = [
    OpeningMonitor("开盘前分析"),
]
for m in monitor:
    schedule.every().day.at(m.time).do(m.start)

print("服务启动成功，现在是北京时间：", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

while True:
    schedule.run_pending()
    time.sleep(1)
