import threading
import time
from datetime import date
from longport.openapi import QuoteContext, Config, Market

config = Config.from_env()
ctx = QuoteContext(config)

def is_trading_days():
    resp = ctx.trading_days(Market.HK, date(2024, 1, 10), date(2024, 1, 17))
    print(resp)

def run_stock_data_monitor_thread():
    """
    1.获取每天开市情况
    2.获取实时股票数据
    3.存储到数据库
    """
    # resp = ctx.trading_session()
    is_trading_days()
    # print(resp)

def run_price_analysis_thread():
    pass

def main():
    stock_data_monitor_thread = threading.Thread(target=run_stock_data_monitor_thread)
    price_analysis_thread = threading.Thread(target=run_price_analysis_thread)
    
    # 设置为守护线程
    stock_data_monitor_thread.daemon = True
    price_analysis_thread.daemon = True
    
    # 启动线程
    stock_data_monitor_thread.start()
    price_analysis_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("程序退出...")

if __name__ == "__main__":
    main()
