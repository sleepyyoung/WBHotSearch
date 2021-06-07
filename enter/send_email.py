import smtplib
from email.mime.text import MIMEText
from email.header import Header
from WBHotSearch import settings


class Mail:
    def __init__(self, receiver, captcha, method):
        self.mail_host = settings.EMAIL_HOST  
        self.mail_port = settings.EMAIL_PORT 
        self.mail_pass = settings.EMAIL_HOST_PASSWORD 
        self.sender = settings.EMAIL_HOST_USER  
        self.from_ = settings.EMAIL_FROM  
        self.receiver = receiver  
        self.captcha = captcha
        self.method = "注册" if method == "register" else "忘记密码" 

    def send(self):
        mail_msg = f"""
        <p>您正在网站 <a href="http://wblsrs.top/"> 微博历史热搜 </a> 利用该邮箱账号进行{self.method}操作</p>
        <p>验证码为 <strong><font size="50px"> {self.captcha} </font></strong></p>
        <p>有效时间5分钟</p>
        <p>如非本人操作，请忽略</p>
        """
        message = MIMEText(mail_msg, 'html', 'utf-8')

        message['From'] = Header(self.from_, 'utf-8')
        message['To'] = Header(self.receiver, 'utf-8')

        message['Subject'] = Header(f"微博历史热搜-{self.method}", 'utf-8')

        smtp_obj = smtplib.SMTP_SSL(self.mail_host, self.mail_port)
        smtp_obj.login(self.sender, self.mail_pass)
        smtp_obj.sendmail(self.sender, self.receiver, message.as_string())
        smtp_obj.quit()


