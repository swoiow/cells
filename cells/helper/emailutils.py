#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

mail_user = os.environ.get("MAIL_USER")
mail_pass = os.environ.get("MAIL_PASS")
mail_server = os.environ.get("MAIL_SERVER")
mail_port = os.environ.get("MAIL_PORT", 465)

assert all([mail_user, mail_pass, mail_server, mail_port])


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def handle_attachment(abs_file):
    part = MIMEApplication(open(abs_file, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(abs_file))
    return part


def send(to_addr, title, mail_body, attachments):
    try:
        msg = MIMEMultipart()

        msg["From"] = _format_addr("<%s>" % mail_user)
        msg["To"] = _format_addr("<%s>" % to_addr)
        msg["Subject"] = Header(title, "utf-8").encode()

        body = MIMEText(mail_body, "plain", "utf-8")
        msg.attach(body)

        if attachments:
            for abs_file_path in attachments:
                msg.attach(handle_attachment(abs_file_path))

        server = smtplib.SMTP_SSL(mail_server, mail_port)
        # server.starttls()
        # server.set_debuglevel(1)

        server.login(mail_user, mail_pass)
        server.sendmail(mail_user, [to_addr], msg.as_string())
        server.quit()

        return dict(result=True)
    except Exception as e:
        return dict(result=False, details=e)
