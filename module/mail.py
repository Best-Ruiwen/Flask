import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def sendmail(addr, code):
    EMAIL_FROM = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_HOST, EMAIL_PORT = '', 80
    replyto = EMAIL_FROM

    content = '您的验证码是：{}'.format(str(code)) + '\n' + '10分钟内有效'
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '[请勿回复]RivenCloud 验证码'
    msg['From'] = '%s <%s>' % ("admin", EMAIL_FROM)
    msg['To'] = '%s <%s>' % ("client", addr)
 
    msg['Reply-to'] = replyto
    msg['Message-id'] = email.utils.make_msgid()
    msg['Date'] = email.utils.formatdate()
    textplain = MIMEText('{}'.format(content), _subtype='plain', _charset='UTF-8')
    msg.attach(textplain)

    try:
        client = smtplib.SMTP()
        client.connect(EMAIL_HOST, EMAIL_PORT)
        client.login(EMAIL_FROM, EMAIL_HOST_PASSWORD)
        client.sendmail(EMAIL_FROM, [addr], msg.as_string())
        client.quit()
        return True

    except:
        return False
        
