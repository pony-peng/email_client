# -*- coding: utf-8 -*-
# @Author  : pony-peng
# @description : send email using smtp and ssl protocol

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import optparse


class SendEmail(object):
 
    def __init__(self):
        super(SendEmail, self).__init__()
 
        # 第三方 SMTP 服务
        self._smtp_host = "smtp.163.com"        # 设置 邮件服务商 服务器
        self._smtp_port = 465                   # 设置 端口
 
        # 默认的发送邮件的邮箱地址和密码。
        # 当没有传递发送者的邮箱地址和密码时，使用默认的邮箱地址和密码发送
        self._email_address = "xxxxxx@163.com"  # 用户名
        self._email_password = "*******"        # 口令

        self.frm = None
        self.pwd = None
        self.to = None
        self.email_title = None
        self.email_content = None
        self.attach_path = None
        self.attach_path_list = None

 
    def set_args(self, frm=None, pwd=None, to=None, email_title=None, email_content=None, attach_path=None):
        """
            设置参数
        :param frm: 发送者邮箱地址
        :param pwd: 发送者邮箱口令
        :param to:  接收者邮箱地址，多个接收者时以逗号','分割
        :param email_title:  邮件标题
        :param email_content:邮件内容
        :param attach_path:  附件路径，多个附件时以逗号','分割
        :return:
        """
        if frm:
            self.frm = frm
            if not pwd:
                raise Exception('设置邮箱密码')
            else:
                self.pwd = pwd
        else:
            self.frm = self._email_address
            self.pwd = self._email_password
        self.to = to
        self.email_title = email_title
        self.email_content = email_content
        self.attach_path = attach_path
 
        # 把逗号分割的附件路径变成 list
        if self.attach_path is not None:
            self.attach_path_list = self.attach_path if ',' not in self.attach_path else self.attach_path.split(',')
 
    def send_email(self):
        multi_part = MIMEMultipart()
        multi_part['From'] = self.frm
        multi_part['To'] = self.to
        multi_part['Subject'] = Header(self.email_title, "utf-8")
 
        # 添加 邮件 内容
        msg = self.email_content
        email_body = MIMEText(msg, 'plain', 'utf-8')
        multi_part.attach(email_body)
 
        # 添加附件
        if isinstance(self.attach_path_list, str):
            # 只有一个附件
            attach = MIMEText(open(self.attach_path, 'rb').read(), 'base64', 'utf-8')
            attach["Content-Type"] = 'application/octet-stream'
 
            # filename not strict
            attach_file_name = self.attach_path_list.split('/')[-1]
            attach["Content-Disposition"] = 'attachment; filename="{0}"'.format(attach_file_name)
            multi_part.attach(attach)
        elif isinstance(self.attach_path_list, list):
            # 多个附件
            for item in self.attach_path_list:
                attach = MIMEText(open(item, 'rb').read(), 'base64', 'utf-8')
                attach["Content-Type"] = 'application/octet-stream'
 
                # filename not strict
                attach_file_name = item.split('/')[-1]
                attach["Content-Disposition"] = 'attachment; filename="{0}"'.format(attach_file_name)
                multi_part.attach(attach)
 
        # ssl 协议安全发送
        smtp_server = smtplib.SMTP_SSL(host=self._smtp_host, port=self._smtp_port)
        try:
            smtp_server.login(self.frm, self.pwd)
            smtp_server.sendmail(self.frm, self.to, multi_part.as_string())
        except smtplib.SMTPException as e:
            print("send fail", e)
        else:
            print("send success")
        finally:
            try:
                smtp_server.quit()
            except smtplib.SMTPException:
                print("quit fail")
            else:
                print("quit success")
 
 
if __name__ == '__main__':
    parse = optparse.OptionParser(
        usage='"usage : %prog [options] arg1,arg2"', version="%prog 1.2"
    )
    parse.add_option(
        '-t', '--to', dest='to', action='store', type=str, metavar='to',
        help='接收者的邮箱地址, 多个接收者时以逗号 "," 分隔'
    )
    parse.add_option(
        '-f', '--from', dest='frm', type=str, metavar='from',
        help='发送者的邮箱地址'
    )
    parse.add_option(
        '-p', '--pwd', dest='pwd', type=str, metavar='pwd',
        help='发送者的邮箱口令'
    )
    parse.add_option(
        '-T', '--title', dest='email_title', type=str, metavar='title',
        help='邮件标题'
    )
    parse.add_option(
        '-C', '--content', dest='email_content', type=str, metavar='content',
        help='邮件内容'
    )
    parse.add_option(
        '-A', '--attach', dest='attach_path', type=str, metavar='attach',
        help='邮件的附件路径, 多个附件时以逗号 "," 分隔'
    )
    parse.add_option('-v', help='help')
 
    options, args = parse.parse_args()
 
    temp_send = SendEmail()
    temp_send.set_args(
        frm=options.frm, pwd=options.pwd, to=options.to,
        email_title=options.email_title,
        email_content=options.email_content,
        attach_path=options.attach_path
    )
    temp_send.send_email()
