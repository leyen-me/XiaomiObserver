import json
from .email import send_email
from .hk import get_rebang_today_news, get_rebang_weibo_news, get_rebang_zhihu_news, get_xiaomi_news, get_xiaomi_dashi, get_all_hk_trend, get_xiaomi_rating
from .hk import get_rebang_diyicaijing_news, get_rebang_eastmoney_news, get_rebang_ithome_news, get_rebang_thepaper_news, get_rebang_toutiao_news, get_rebang_xueqiu_news
from .query import client, model
from .constans import system_prompt
from .hk import get_dingpan_hk_trend


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

    def try_get_news(self, func):
        try:
            return func()
        except Exception as e:
            print(e)
            return "新闻获取失败"

    def run(self):
        rebang_today_news = self.try_get_news(get_rebang_today_news)
        rebang_zhihu_news = self.try_get_news(get_rebang_zhihu_news)
        rebang_weibo_news = self.try_get_news(get_rebang_weibo_news)
        rebang_ithome_news = self.try_get_news(get_rebang_ithome_news)
        rebang_thepaper_news = self.try_get_news(get_rebang_thepaper_news)
        rebang_toutiao_news = self.try_get_news(get_rebang_toutiao_news)
        rebang_xueqiu_news = self.try_get_news(get_rebang_xueqiu_news)
        rebang_eastmoney_news = self.try_get_news(get_rebang_eastmoney_news)
        rebang_diyicaijing_news = self.try_get_news(
            get_rebang_diyicaijing_news)
        rebang_news = rebang_today_news + '\n' + rebang_zhihu_news + '\n' + rebang_weibo_news + '\n' + rebang_ithome_news + '\n' + \
            rebang_thepaper_news + '\n' + rebang_toutiao_news + '\n' + rebang_xueqiu_news + '\n' + \
            rebang_eastmoney_news + '\n' + rebang_diyicaijing_news

        try:
            xiaomi_dashi = json.dumps(get_xiaomi_dashi())
            xiaomi_news = json.dumps(get_xiaomi_news())
            xiaomi_rating = json.dumps(get_xiaomi_rating())
        except Exception as e:
            print(e)
            xiaomi_dashi = "小米大事件获取失败"
            xiaomi_news = "小米新闻获取失败"
            xiaomi_rating = "小米投资评级获取失败"

            rebang_news = """# 今日新闻""" + "\n" + rebang_news + "\n" + """# 小米相关大事件""" + "\n" + xiaomi_dashi + \
                "\n" + """# 小米相关新闻""" + "\n" + xiaomi_news + \
                "\n" + """# 小米相关投资评级""" + "\n" + xiaomi_rating

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "今天的新闻是什么?"},
                {"role": "assistant", "content": rebang_news},
                {"role": "user", "content": "请根据这些信息给出小米股票当日的分析和建议，如果你有自己独到的见解，请在最后给出你的独到见解。"},
            ],
        )
        return response.choices[0].message.content




class DingPanMonitor:
    def __init__(self, name):
        super().__init__(name)
        self.time = "09:30"

    def run(self):
        try:
            trend_data = get_dingpan_hk_trend()
            if trend_data:
                return f"盯盘数据收集完成，共收集 {len(trend_data)} 条数据点"
            return "未收集到盯盘数据"
        except Exception as e:
            print(f"盯盘监控异常: {e}")
            return "盯盘监控执行失败"

