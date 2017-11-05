#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

mail_user = os.environ.get("MAIL_USER")
mail_pass = os.environ.get("MAIL_PASS")
mail_server = os.environ.get("MAIL_SERVER")
mail_port = os.environ.get("MAIL_PORT")

assert all([mail_user, mail_pass, mail_server, mail_port])


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send(to_addr, title, mail_body):
    try:
        msg = MIMEText(mail_body, "plain", "utf-8")
        msg["From"] = _format_addr("<%s>" % mail_user)
        msg["To"] = _format_addr("<%s>" % to_addr)
        msg["Subject"] = Header(title, "utf-8").encode()

        server = smtplib.SMTP(mail_server, mail_port)
        server.starttls()
        # server.set_debuglevel(1)

        server.login(mail_user, mail_pass)
        server.sendmail(mail_user, [to_addr], msg.as_string())
        server.quit()

        return dict(result=True)
    except Exception as e:
        return dict(result=False, details=e)
