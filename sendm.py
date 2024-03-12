import smtplib
from email.message import EmailMessage

def mail_to_send_me(maildata):
    email_address_from = '2074494853@qq.com'
    email_address = '1430147707@qq.com'
    email_title = '空教室用户报告'
    email_content = maildata
    message = EmailMessage()
    message['Subject'] = email_title
    message['From'] = email_address_from
    message['To'] = email_address
    message.set_content(email_content)

# 发送邮件
    with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
        server.login(email_address_from, '')

        server.send_message(message)

