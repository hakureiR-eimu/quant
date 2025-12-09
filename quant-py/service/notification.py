import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import datetime
import os
import json

class EmailNotifier:
    """邮件通知器"""
    
    def __init__(self,config_file='config.json'):
        # 读取配置
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        email_config = config.get('email', {})
        self.smtp_server = email_config.get('smtp_server')
        self.smtp_port = email_config.get('smtp_port')
        self.sender = email_config.get('sender')
        self.password = email_config.get('password')
        self.receivers = email_config.get('receivers', [])
    
    def send(self, subject, content):
        """
        发送邮件
        :param subject: 邮件主题
        :param content: 邮件内容
        """
        try:
            # 创建邮件对象
            message = MIMEMultipart()
            message['From'] = f"量化交易助手 <{self.sender}>"
            message['To'] = ','.join(self.receivers)
            message['Subject'] = subject
            
            # 添加邮件正文
            message.attach(MIMEText(content, 'plain', 'utf-8'))
            
            # 发送邮件
            if self.smtp_port == 465:
                # SSL连接
                server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            else:
                # TLS连接
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
            
            server.login(self.sender, self.password)
            server.sendmail(self.sender, self.receivers, message.as_string())
            server.quit()
            
            print(f"✓ 邮件发送成功: {subject}")
            return True
            
        except Exception as e:
            print(f"✗ 邮件发送失败: {e}")
            return False


# 全局邮件通知器实例
_email_notifier = EmailNotifier()


def notify(message: str):
    """
    发送通知消息
    :param message: 通知内容
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    subject = f"【量化交易信号】{timestamp}"
    content = f"{message}\n\n时间: {timestamp}"
    
    # 同时打印到控制台
    print(f"\n📧 {message}")
    
    # 发送邮件
    _email_notifier.send(subject, content)