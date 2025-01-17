import os

xiaomi_stock_code = "1810.HK"

qq_email = os.getenv("QQ_EMAIL")
qq_email_authorization_code = os.getenv("QQ_EMAIL_AUTHORIZATION_CODE")
qq_email_host = 'smtp.qq.com'

system_prompt = """You are a professional Xiaomi stock analyst."""

def get_question_prompt(desc):
    return f"""
Please analyze {desc} based on the information provided above, Answer in Chinese。

The user will provide some exam text. Please parse the "isCanBuy" and "reason" and output them in JSON format. 

EXAMPLE INPUT: 
Is today a good day to buy Xiaomi stock?

EXAMPLE JSON OUTPUT:
{{
    "isCanBuy": true,
    "reason": "because..."
}}
"""