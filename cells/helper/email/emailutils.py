#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import smtplib
import traceback
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

from . import mail_server


def _format_addr(s):
    name, addr = parseaddr(s)
    pair = (Header(name, 'utf-8').encode(), addr)
    return formataddr(pair=pair)


def handle_attachment(abs_file):
    part = MIMEApplication(open(abs_file, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(abs_file))
    return part


class MailClient(object):
    def __init__(self, username=None, password=None, alias=None, *args, **kwargs):
        self.MAIL_USER = username or os.environ.get("MAIL_USER")
        self.MAIL_PASS = password or os.environ.get("MAIL_PASS")

        self.MAIL_IN_SERVER = os.environ.get("MAIL_IN_SERVER", os.environ.get("MAIL_SERVER"))
        self.MAIL_IN_PORT = os.environ.get("MAIL_IN_PORT", os.environ.get("MAIL_PORT"))

        self.MAIL_OUT_SERVER = os.environ.get("MAIL_OUT_SERVER", os.environ.get("MAIL_SERVER"))
        self.MAIL_OUT_PORT = os.environ.get("MAIL_OUT_PORT", os.environ.get("MAIL_PORT"))

        self._search_config(alias=alias)

    def send(
            self, to_addr, title, body,
            cc_addr=None, bcc_addr=None, attachments=None,
            *args, **kwargs
    ):

        self._prepare()

        mail_receiver = []

        msg = MIMEMultipart()

        msg["From"] = _format_addr("<%s>" % self.MAIL_USER)
        msg["Subject"] = Header(title, "utf-8").encode()

        if isinstance(to_addr, (str, bytes)):
            to_addr = [to_addr]

        msg["To"] = ",".join([_format_addr("<%s>" % addr) for addr in to_addr])
        mail_receiver.extend(to_addr)

        if cc_addr:
            if isinstance(cc_addr, (str, bytes)): cc_addr = [cc_addr]

            msg["Cc"] = ",".join([_format_addr("<%s>" % addr) for addr in cc_addr])
            mail_receiver.extend(cc_addr)

        if bcc_addr:
            if isinstance(bcc_addr, (str, bytes)): bcc_addr = [bcc_addr]

            msg["Bcc"] = ",".join([_format_addr("<%s>" % addr) for addr in bcc_addr])
            mail_receiver.extend(bcc_addr)

        body = MIMEText(body, _charset="utf-8")
        msg.attach(body)

        if attachments:
            assert isinstance(attachments, list)

            for abs_file_path in attachments:
                msg.attach(handle_attachment(abs_file_path))

        try:
            server = smtplib.SMTP_SSL(self.MAIL_OUT_SERVER, self.MAIL_OUT_PORT)
            # server.starttls()
            # server.set_debuglevel(1)
            server.login(self.MAIL_USER, self.MAIL_PASS)

            server.sendmail(self.MAIL_USER, mail_receiver, msg.as_string())
            server.quit()

            return dict(result=True)

        except Exception as e:
            # 可以调用 self._search_config(refresh=True)
            return dict(result=False, details=traceback.format_exc())

    def _search_config(self, alias=None, refresh=False):

        alias = alias or os.environ.get("MAIL_PROVIDER")
        config = None
        objs = (getattr(mail_server, obj) for obj in dir(mail_server) if obj.startswith("Mail"))

        if alias:
            for obj in objs:
                if alias in getattr(obj, "_alias", []):
                    config = obj
                    break

        else:
            user_domain = self.MAIL_USER.split("@")[-1]
            for obj in objs:
                if user_domain in getattr(obj, "smtp_out_server", ""):
                    config = obj
                    break

                elif any(map(lambda m: user_domain.find(m) > -1, getattr(obj, "_alias", []))):
                    config = obj
                    break

        if config:
            # TODO: refresh 时，更换端口

            self._MAIL_PROVIDER_SETTINGS = config

            if not self.MAIL_IN_SERVER or refresh:
                self.MAIL_IN_SERVER = config.pop3_in_server or config.imap_in_server
            if not self.MAIL_IN_PORT or refresh:
                self.MAIL_IN_PORT = config.pop3_in_port

            if not self.MAIL_OUT_SERVER or refresh:
                self.MAIL_OUT_SERVER = config.smtp_out_server
            if not self.MAIL_OUT_PORT or refresh:
                self.MAIL_OUT_PORT = config.smtp_out_ssl_port or config.smtp_out_tls_port

    def _prepare(self, type_="out"):
        if type_ == "in":
            attrs = ["MAIL_USER", "MAIL_PASS", "MAIL_IN_SERVER", "MAIL_IN_PORT"]
        else:
            attrs = ["MAIL_USER", "MAIL_PASS", "MAIL_OUT_SERVER", "MAIL_OUT_PORT"]

        for attr in attrs:
            if not getattr(self, attr):
                print("\n\nERROR: {} is missing.\n".format(attr))
                break

        return exit(0)
