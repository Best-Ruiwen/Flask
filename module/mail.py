import smtplib
from email.mime.text import MIMEText
from email.header import Header


def sendmail(addr, code):
    sender = 'riven@cloud.com'
    receivers = [addr]  # 接收邮件地址
    print(code)

    message = MIMEText('您的验证码是:{}'.format(str(code))+ '\n' + '10分钟内有效', 'plain')
    message['From'] = Header("rivencloud")  # 发送者
    message['To'] = Header("", '')  # 接收者

    subject = 'RivenCloud验证码'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message.as_string())
        return True
    except smtplib.SMTPException:
        return False
