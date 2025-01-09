import json
import time
import requests
from longport.openapi import QuoteContext, Config, SubType, PushQuote

config = Config.from_env()

STOCKS = {
    "300750.SZ": "宁德时代",
    "1810.HK": "小米集团",
    "700.HK": "腾讯控股",
    "9988.HK": "阿里巴巴",
    "3690.HK": "美团",
    "388.HK": "香港交易所",
}


def get_all_hk_trend():
    """
    获取所有股数据(包含内地港股和香港港股)，判断港股整体是上涨还是下跌趋势
    """
    res = {
        "schema": {
            "symbol": "股票代码",
            "name": "股票名称",
            "open_price": "开盘价",
            "last_done": "最新价",
            "decline_rate": "下跌幅度",
            "change": "涨跌"
        },
        "data": []
    }

    def on_quote(symbol: str, event: PushQuote):
        open_price = float(event.open)
        last_done = float(event.last_done)
        stock_data = {
            "symbol": symbol,
            "name": STOCKS[symbol],
            "open_price": open_price,
            "last_done": last_done,
            "decline_rate": (last_done - open_price) / open_price,
            "change": '下跌' if last_done - open_price < 0 else '上涨'
        }
        try:
            res["data"].append(stock_data)
        except Exception as e:
            print(e)
        print(stock_data)

    ctx = QuoteContext(config)
    ctx.set_on_quote(on_quote)

    # 订阅股票
    symbols = [symbol for symbol in STOCKS.keys()]
    ctx.subscribe(symbols, [SubType.Quote], is_first_push=True)

    # 等待所有股票数据
    while len(res["data"]) < len(STOCKS):
        time.sleep(1)
    return res


def get_xiaomi_dashi():
    """
    获取小米最近大事件
    """
    url = "https://datacenter.eastmoney.com/securities/api/data/get?type=RPT_F10_HK_INDEX&params=01810.HK&p=1&source=F10&client=PC"
    res = requests.get(url)
    data = json.loads(res.text)["data"]
    return data


def get_xiaomi_news():
    """
    获取小米最近资讯
    """
    url = "https://emdcnewsapp.eastmoney.com/infoService"
    data = {"args": {"market": "116", "pageNumber": "1", "pageSize": "5", "securityCode": "01810",
                     "fields": "code,infoCode,title,showDateTime,summary,url,uniqueUrl"}, "method": "securityNews"}
    res = requests.post(url, data=json.dumps(data))
    data = json.loads(res.text)["data"]['items']
    return data


def get_xiaomi_rating():
    """
    获取小米投资评级
    """
    params = {
        "reportName": "RPT_HKPCF10_INFO_ORGRATING",
        "columns": "SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,ORG_CODE,ORG_NAME,RATING_NAME,PRE_RATING_NAME,TARGET_PRICE,PRE_TARGET_PRICE,TARGET_PRICE_CHANGE,PUBLISH_DATE",
        "quoteColumns": "",
        "filter": "(SECUCODE=\"01810.HK\")",
        "pageNumber": 1,
        "pageSize": 10,
        "sortTypes": -1,
        "sortColumns": "PUBLISH_DATE",
        "source": "F10",
        "client": "PC",
    }
    base_url = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
    res = requests.get(base_url, params=params)
    data = json.loads(res.text)["result"]['data']
    return data
