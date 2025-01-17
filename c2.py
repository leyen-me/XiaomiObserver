import datetime
import threading
import time
import schedule


def get_xiaomi_price():
    """获取小米股价并保存到数据库"""
    print(f"[{datetime.now()}] 获取小米每日股价...")
    # TODO: 实现获取小米股价的逻辑
    # TODO: 保存到数据库

def analyze_stock_prices():
    """每5分钟获取股价并分析支撑位和阻力位"""
    print(f"[{datetime.now()}] 分析股价支撑位和阻力位...")
    # TODO: 实现获取股价的逻辑
    # TODO: 调用 AI 分析支撑位和阻力位

def run_schedule(scheduler):
    """运行定时任务"""
    while True:
        scheduler.run_pending()
        time.sleep(1)

def main():
    # 创建两个独立的 schedule 实例
    xiaomi_scheduler = schedule.Scheduler()
    analysis_scheduler = schedule.Scheduler()

    xiaomi_scheduler.every().day.at("09:30").do(get_xiaomi_price)

    analysis_scheduler.every().day.at("09:30").do(analyze_stock_prices)
    analysis_scheduler.every(5).minutes.do(analyze_stock_prices)

    thread1 = threading.Thread(target=run_schedule, args=(xiaomi_scheduler,))
    thread2 = threading.Thread(target=run_schedule, args=(analysis_scheduler,))
    
    thread1.daemon = True
    thread2.daemon = True

    thread1.start()
    thread2.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("程序退出...")


if __name__ == "__main__":
    main()