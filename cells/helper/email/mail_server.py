#!/usr/bin/env python
# -*- coding: utf-8 -*


class _mail(object):
    """ https://support.google.com/mail/answer/7126229?hl=en """

    pop3_in_server = None
    pop3_in_port = 110
    pop3_in_ssl_port = 995

    imap_in_server = None
    imap_in_port = 143
    imap_in_ssl_port = 993

    smtp_out_server = None
    smtp_out_port = 25
    smtp_out_ssl_port = 465
    smtp_out_tls_port = 587

    _alias = []


class MailAli(_mail):
    """ https://help.aliyun.com/knowledge_detail/36576.html """

    pop3_in_server = "pop3.mxhichina.com"
    imap_in_server = "imap.mxhichina.com"
    smtp_out_server = "smtp.mxhichina.com"

    _alias = ["ali", "aliyun", "alimail"]


class MailGmail(_mail):
    pop3_in_server = "pop.gmail.com"
    imap_in_server = "imap.gmail.com"
    smtp_out_server = "smtp.gmail.com"


class MailOutlook(_mail):
    """ https://support.office.com/en-us/article/d088b986-291d-42b8-9564-9c414e2aa040 """

    pop3_in_server = "pop-mail.outlook.com"
    imap_in_server = "imap-mail.outlook.com"
    smtp_out_server = "smtp-mail.outlook.com"

    _alias = ["live", "hotmail"]


MailHotmail = MailOutlook


class MailQQ(_mail):
    """ http://service.mail.qq.com/cgi-bin/help?subtype=1&id=28&no=369 """

    pop3_in_server = "pop.qq.com"
    smtp_out_server = "smtp.qq.com"


class MailExQQ(_mail):
    """ http://service.exmail.qq.com/cgi-bin/help?id=28&no=1000585&subtype=1 """

    pop3_in_server = "pop.exmail.qq.com "
    imap_in_server = "imap.exmail.qq.com"
    smtp_out_server = "smtp.exmail.qq.com"

    def node(self):
        self.pop3_in_server = "hwpop.exmail.qq.com"
        self.imap_in_server = "hwimap.exmail.qq.com"
        self.smtp_out_server = "hwsmtp.exmail.qq.com"


class MailYeah(_mail):
    """ http://mail.21cn.com/weiyou/help.html """

    pop3_in_server = "pop.yeah.net"
    imap_in_server = "imap.yeah.net"
    smtp_out_server = "smtp.yeah.net"


class Mail163(_mail):
    """ http://help.163.com/09/1223/14/5R7P3QI100753VB8.html """

    pop3_in_server = "pop.163.com"
    imap_in_server = "imap.163.com"
    smtp_out_server = "smtp.163.com"


class Mail126(_mail):
    """ http://help.163.com/09/0219/10/52GOPOND007536NI.html """

    pop3_in_server = "pop.126.com"
    imap_in_server = "imap.126.com"

    smtp_out_server = "smtp.126.com"
    smtp_out_tls_port = 994


class MailSina(_mail):
    """ http://mail.21cn.com/weiyou/help.html """

    pop3_in_server = "pop.sina.com"
    imap_in_server = "imap.sina.com"
    smtp_out_server = "smtp.sina.com"


class MailSohu(_mail):
    """ http://mail.21cn.com/weiyou/help.html """

    pop3_in_server = "pop3.sohu.com"
    imap_in_server = "imap.sohu.com"
    smtp_out_server = "smtp.sohu.com"
