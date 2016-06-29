# coding:utf8

"""
Copyright 2016 Smallpay Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import smtplib
from email.mime.text import MIMEText
from stockquant.utils.log import logger

class Mail(object):

    _user = '18611736372@163.com'
    _to = 'tufei8438@gmail.com'
    _pwd = 'feitu1994'
    _smtp = 'smtp.163.com'

    def send(self, subject, content, subtype='plain', from_=None, to_=None):
        msg = MIMEText(content, _subtype=subtype, _charset='utf-8')
        msg["Subject"] = subject
        msg["From"] = from_ or self._user
        msg["To"] = to_ or self._to

        try:
            smtp = smtplib.SMTP_SSL(self._smtp, timeout=30)
            smtp.login(self._user, self._pwd)
            smtp.sendmail(self._user, self._to, msg.as_string())
            smtp.close()
            return True
        except smtplib.SMTPException:
            logger.exception("邮件发送失败。主题:[%s] 内容:[%s]" % (subject, content))
            return False
