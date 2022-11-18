import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dap_config.read_config import Read_Config


class Mail:
    # 获取email.ini配置文件的数据

    def __init__(self):
        self.msg = None
        self.config = Read_Config('/dap_config/email.ini').read_emailini('email')
        self.con = smtplib.SMTP_SSL(self.config['SMTP_SSL'], int(self.config['port']))
        self.con.login(user=self.config['user'], password=self.config['password'])

    def MIMEMultipart(self):
        self.msg = MIMEMultipart()

    def send_image(self, file_name, file_type):
        html_file = open(file_name, 'rb').read()
        image_data = MIMEText(html_file, file_type, 'utf-8')
        self.msg.attach(image_data)

    def sent_files(self, file_reports, file_type, filename):
        html_file = open(file_reports, 'rb').read()
        atr1 = MIMEText(html_file, file_type, 'utf-8')
        atr1["Content-Type"] = 'application/octet-stream'
        atr1['Content-Disposition'] = 'attachment; filename="%s"' % filename
        self.msg.attach(atr1)
        msg = MIMEText('任务编排系统自动化接口测试报告', file_type, 'utf-8')
        self.msg.attach(msg)

    def send_mail(self, subject):
        # 主题
        self.msg['subject'] = subject
        # 发送人
        self.msg['from'] = self.config['sender']
        # 收件人
        self.msg['to'] = ';'.join([self.config['receive']])
        # 抄送人
        self.msg['Cc'] = ';'.join([self.config['Cc']])
        # 发送邮件
        self.con.sendmail(self.config['sender'], self.config['receive'], self.msg.as_string())

    def quit(self):
        self.con.quit()


if __name__ == '__main__':
    send = Mail()
    send.MIMEMultipart()
    send.send_image(r'C:\Users\DELL\PycharmProjects\dapSystem_Api\log\2022_11_18.log', 'html')
    send.send_mail('任务编排系统自动化接口测试报告')
