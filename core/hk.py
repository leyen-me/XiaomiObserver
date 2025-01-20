import json
import time
import requests
from longport.openapi import QuoteContext, Config, SubType, PushQuote, TradeContext
from .constans import xiaomi_stock_code, rebang_today_base_url, common_header, rebang_today_name

config = Config.from_env()
quoteContext = QuoteContext(config)
tradeContext = TradeContext(config)

STOCKS = {
    "300750.SZ": "宁德时代",
    xiaomi_stock_code: "小米集团",
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

    quoteContext.set_on_quote(on_quote)

    # 订阅股票
    symbols = [symbol for symbol in STOCKS.keys()]
    quoteContext.subscribe(symbols, [SubType.Quote], is_first_push=True)

    # 等待所有股票数据
    while len(res["data"]) < len(STOCKS):
        time.sleep(1)

    quoteContext.unsubscribe(symbols, [SubType.Quote])
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

def get_rebang_today_news():
    """
    rebang.today 综合新闻
    """
    params = {
        "tab": "top",
        "sub_tab": "today",
        "page": 1,
        "version": 1
    }
    base_url = f"{rebang_today_base_url}/v1/items"
    res = requests.get(base_url, params=params, headers=common_header)
    data = json.loads(res.json()['data']['list'])
    content = f"""## `{rebang_today_name}`综合新闻\n\n"""
    for item in data:
        content += f"""- {item['title']}({'暂无描述' if item['desc'] == '' else item['desc']})\n"""
    return content

def get_rebang_zhihu_news():
    """
    rebang.today 知乎新闻
    """
    params = {
        "tab": "zhihu",
        "date_type": "now",
        "page": 1,
        "version": 1
    }
    base_url = f"{rebang_today_base_url}/v1/items"
    res = requests.get(base_url, params=params, headers=common_header)
    data = json.loads(res.json()['data']['list'])
    content = f"""## `{rebang_today_name}`知乎新闻\n\n"""
    for item in data:
        content += f"""- {item['title']}({'暂无描述' if item['describe'] == '' else item['describe']})\n"""
    return content

def get_rebang_weibo_news():
    """
    rebang.today 微博新闻
    """
    params = {
        "tab": "weibo",
        "sub_tab": "news",
        "page": 1,
        "version": 2
    }
    base_url = f"{rebang_today_base_url}/v1/items"
    res = requests.get(base_url, params=params, headers=common_header)
    data = json.loads(res.json()['data']['list'])
    content = f"""## `{rebang_today_name}`微博新闻\n\n"""
    for item in data:
        content += f"""- {item['title']}\n"""
    return content

def get_rebang_ithome_news():
    """
    rebang.today IT之家新闻
    """
    params = {
        "tab": "ithome",
        "sub_tab": "today",
        "page": 1,
        "version": 1
    }
    base_url = f"{rebang_today_base_url}/v1/items"
    res = requests.get(base_url, params=params, headers=common_header)
    data = json.loads(res.json()['data']['list'])
    content = f"""## `{rebang_today_name}`IT之家新闻\n\n"""
    for item in data:
        content += f"""- {item['title']}({'暂无描述' if item['desc'] == '' else item['desc']})\n"""
    return content

def get_rebang_thepaper_news():
    """
    rebang.today 澎湃新闻
    """
    params = {
        "tab": "thepaper", 
        "sub_tab": "hot",
        "page": 1,
        "version": 1
    }
    base_url = f"{rebang_today_base_url}/v1/items"
    res = requests.get(base_url, params=params, headers=common_header)
    data = json.loads(res.json()['data']['list'])
    content = f"""## `{rebang_today_name}`澎湃新闻\n\n"""
    for item in data:
        content += f"""- {item['title']}({'暂无描述' if item['desc'] == '' else item['desc']})\n"""
    return content

def get_rebang_toutiao_news():
    """
    rebang.today 头条新闻
    """
    params = {
        "tab": "toutiao",
        "page": 1,
        "version": 1
    }
    base_url = f"{rebang_today_base_url}/v1/items"
    res = requests.get(base_url, params=params, headers=common_header)
    data = json.loads(res.json()['data']['list'])
    content = f"""## `{rebang_today_name}`头条新闻\n\n"""
    for item in data:
        content += f"""- {item['title']}\n"""
    return content

def get_rebang_xueqiu_news():
    """
    rebang.today 雪球新闻
    """
    params = {
        "tab": "xueqiu",
        "sub_tab": "topic",
        "page": 1,
        "version": 1
    }
    base_url = f"{rebang_today_base_url}/v1/items"
    res = requests.get(base_url, params=params, headers=common_header)
    data = json.loads(res.json()['data']['list'])
    content = f"""## `{rebang_today_name}`雪球新闻\n\n"""
    for item in data:
        content += f"""- {item['title']}({'暂无描述' if item['desc'] == '' else item['desc']})\n"""
    return content

def get_rebang_eastmoney_news():
    """
    rebang.today 东方财富新闻
    """
    params = {
        "tab": "eastmoney",
        "sub_tab": "news",
        "page": 1,
        "version": 1
    }
    base_url = f"{rebang_today_base_url}/v1/items"
    res = requests.get(base_url, params=params, headers=common_header)
    data = json.loads(res.json()['data']['list'])
    content = f"""## `{rebang_today_name}`东方财富新闻\n\n"""
    for item in data:
        content += f"""- {item['title']}({'暂无描述' if item['desc'] == '' else item['desc']})\n"""
    return content

def get_rebang_diyicaijing_news():
    """
    rebang.today 第一财经新闻
    """
    params = {
        "tab": "diyicaijing",
        "sub_tab": "headline",
        "page": 1,
        "version": 1
    }
    base_url = f"{rebang_today_base_url}/v1/items"
    res = requests.get(base_url, params=params, headers=common_header)
    data = json.loads(res.json()['data']['list'])
    content = f"""## `{rebang_today_name}`第一财经新闻\n\n"""
    for item in data:
        content += f"""- {item['title']}({'暂无描述' if item['desc'] == '' else item['desc']})\n"""
    return content
