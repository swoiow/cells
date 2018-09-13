#!/usr/bin/env python
# -*- coding: utf-8 -*

from ...helper.email import MailClient


def mod(args=None):
    import argparse

    parser = argparse.ArgumentParser(prog="cells.mods.email", description="Send mail quickly")

    parser.add_argument("-t", dest="title", metavar="title", required=True,
                        help="title of the mail .")
    parser.add_argument("-b", dest="body", metavar="body", required=True,
                        help="body of the mail .")
    parser.add_argument("-U", dest="username", metavar="username", required=True,
                        help="username for mail server login.")
    parser.add_argument("-P", dest="password", metavar="password", required=True,
                        help="password for mail server login.")
    parser.add_argument("--to", dest="to_addr", nargs="*",
                        help="recipient of the mail.")
    parser.add_argument("--ali", dest="alias", nargs="?",
                        help="you mail server provider.")

    parser.add_argument("--cc", dest="cc_addr", nargs="*",
                        help="Cc of the mail.")
    parser.add_argument("--bcc", dest="bcc_addr", nargs="*",
                        help="Bcc of the mail.")
    parser.add_argument("--at", dest="attachments", metavar="PATH", nargs="*",
                        help="full file paths, split with ' '.")

    options = parser.parse_args(args)

    print(options)

    mail = MailClient(
        **vars(options)
    )
    result = mail.send(
        **vars(options)
    )
    print(result)
    return


if __name__ == "__main__":
    mod()
