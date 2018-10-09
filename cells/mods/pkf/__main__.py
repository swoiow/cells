#!/usr/bin/env python
# -*- coding: utf-8 -*


def tar_object(pwd, filename=None, mode=None, enc_mode=None):
    import os, uuid

    if not filename:
        filename = "*"
    if not enc_mode:
        enc_mode = "aes192"

    if mode == "e":
        fid = uuid.uuid4().hex
        c = "tar -czf - {fn} | openssl enc -e -{em} -k {pwd} | dd of=_{fid}.enc"
        c = c.format(fn=filename, pwd=pwd, fid=fid, em=enc_mode)
        os.system(c)

        print("Encrypt Finish !!")

    elif mode == "d":
        c = "dd if={fn} | openssl enc -d -{em} -k {pwd} | tar zxf -"
        c = c.format(fn=filename, pwd=pwd, em=enc_mode)

        os.system(c)
        print("Decrypt Finish !!")

    else:
        print("Unknown Mode !!!")


def mod(args=None):
    import argparse

    parser = argparse.ArgumentParser(prog="cells.mods.pkf", description="tar file with password .")

    parser.add_argument("-f", dest="filename", metavar="filename", required=False, default="*",
                        help="Encrypt file, default: * .")
    parser.add_argument("-p", dest="pwd", metavar="pwd", required=True,
                        help="Encrypt password .")
    parser.add_argument("-m", dest="mode", metavar="mode", required=False, default="e",
                        help="Encrypt(e) / Decrypt(d), default: e  .")
    parser.add_argument("-E", dest="enc_mode", metavar="enc_mode", required=False, default="aes192",
                        help="See 'openssl enc -h' .")

    options = parser.parse_args(args)

    tar_object(**vars(options))


if __name__ == "__main__":
    mod()
