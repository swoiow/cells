#!/usr/bin/env python
# -*- coding: utf-8 -*


def tar_object(pwd, filename=None, mode=None, enc_mode=None, gz=False):
    import os, uuid

    tar_mod, end = "J", "xz"
    if gz:
        tar_mod, end = "z", "gz"

    if not filename:
        filename = "*"
    if not enc_mode:
        enc_mode = "aes192-wrap"

    plus = "-pbkdf1"
    check_openssl_version = os.popen("openssl version").read()
    if check_openssl_version.find(" 1.1") > 0:
        plus = "-pbkdf2"

    if mode == "e":
        c = "tar c{mod}f - {fn} | openssl enc -{em} {plus} -e -k {pwd} | dd of=_{fid}.enc.{end}"
        c = c.format(
            fn=filename, pwd=pwd, mod=tar_mod, fid=uuid.uuid4().hex,
            em=enc_mode, plus=plus, end=end
        )
        print(c)

        os.system(c)
        print("Encrypt Finish !!")

    elif mode == "d":
        tar_mod = "z" if filename.endswith("gz") else "J"

        c = "dd if={fn} | openssl enc -{em} {plus} -d -k {pwd} | tar x{mod}f -"
        c = c.format(
            fn=filename, pwd=pwd, mod=tar_mod,
            em=enc_mode, plus=plus
        )
        print(c)

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
                        help="Encrypt(e) / Decrypt(d), default: e .")
    parser.add_argument("-E", dest="enc_mode", metavar="enc_mode", required=False, default="aes192",
                        help="See 'openssl enc -h' .")
    parser.add_argument("--gz", dest="gz", required=False, default=None,
                        action='store_true',
                        help="Tar file with gz mode. default xz .")

    options = parser.parse_args(args)

    tar_object(**vars(options))


if __name__ == "__main__":
    mod()
