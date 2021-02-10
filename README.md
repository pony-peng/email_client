# email_client
Email_client presents a demo to show how to send email based on smtp and ssl protocol in Python.

## how to use

### make your email ready
 (taking 163 mail as an example)
1. login your 163 email account and go to setting->POP3/SMTP/IMAP to open the IMAP/SMTP service.
2. after you open the IMAP/SMTP service, you will get a token.
3. input your own email account for self._email_address and input the token from step2 for self._email_password.

### send email
python send_email.py -t xxxxxx@qq.com -T title -C test_content

### notice
If you want to use other email service provider such as qq, you also need to change smtp.163.com to smtp.qq.com
