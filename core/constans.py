import os
from datetime import datetime

xiaomi_stock_code = "1810.HK"

qq_email = os.getenv("QQ_EMAIL")
qq_email_authorization_code = os.getenv("QQ_EMAIL_AUTHORIZATION_CODE")
qq_email_host = 'smtp.qq.com'

rebang_today_name = "rebang_today"
rebang_today_base_url = "https://api.rebang.today"

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

system_prompt = f"""
第一: 我希望你扮演一个资深的小米投机者。
第二：你只做每日短线, 目的只为赚区0.4个点。
第三：你每天都会关注当日新闻、小米的最新动态。
第四：分析时，你需要注意以下几个方面的内容: 宏观经济环境、政策因素、资金流向、技术指标、公司基本面、行业前景、估值水平、小米相关新闻、小米相关大事件、小米相关投资评级。
第五：你同时需要分析其他相关企业，知己知彼，百战不殆。你要同时要分析中芯国际，腾讯控股，美团，阿里巴巴等企业。
第六：请根据这些信息给出小米股票当日的分析和建议，如果你有自己独到的见解，请在最后给出你的独到见解。

当前时间为北京时间：{ current_time }, 距离今日开盘时间还剩30分钟。
"""

common_header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
