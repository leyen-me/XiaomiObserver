import yagmail
from core.constans import qq_email, qq_email_authorization_code, qq_email_host

yag = yagmail.SMTP(user=qq_email,
                   password=qq_email_authorization_code,
                   host=qq_email_host)


def send_email(subject, content):
    try:
        yag.send(to=qq_email, subject=subject, contents=content)
        print("邮件发送成功！")
    except Exception as e:
        print(f"发送失败: {e}")
