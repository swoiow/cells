#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import win32api
import win32con
import win32gui
import win32ui
from PIL import ImageGrab

CUT_SLEEP = 1
INTER_SLEEP = 0.2
mouse_event = win32api.mouse_event
keybd_event = win32api.keybd_event
DisplaySize = lambda: (win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))


class KeyMap(object):
    """
    detail: https://segmentfault.com/a/1190000005828048
    control_key_value: Only support LowerCase or CapitalizeCase
    """

    _alphabet_lower = "abcdefghijklmnopqrstuvwxyz"
    _number_ = "0123456789"
    _meta_ = dict()

    def __init__(self):
        x = 48
        for num in self._number_:
            self._meta_[num] = x
            x += 1

        x = 65
        for alpha in self._alphabet_lower:
            self._meta_[alpha] = x
            x += 1

        control_keys = [
            ("BackSpace", 8),
            ("Tab", 9),
            ("Clear", 12),
            ("Enter", 13),
            ("Shift", 16),
            ("Control", 17),
            ("Alt", 18),
            ("CapeLock", 20),
            ("Esc", 27),
            ("Spacebar", 32),
            ("PageUp", 33),
            ("PageDown", 34),
            ("End", 35),
            ("Home", 36),
            ("LeftArrow", 37),
            ("UpArrow", 38),
            ("RightArrow", 39),
            ("DwArrow", 40),
            ("Insert", 45),
            ("Delete", 46),
            ("NumLock", 144),
        ]
        self._meta_.update({k.lower(): v for k, v in control_keys})
        self._meta_.update({k.capitalize(): v for k, v in control_keys})

        shift = self._meta_["shift"]
        for alpha in self._alphabet_lower:
            self._meta_[alpha.upper()] = (shift, self._meta_[alpha])

        py_simple = []
        py_special = [("\\", 220), ("'", 222), ('"', (shift, 222)), ]
        _py_simple = [
            (";:", 186),
            ("=+", 187),
            (",<", 188),
            ("-_", 189),
            (".>", 190),
            ("/?", 191),
            ("`~", 192),
            ("[{", 219),
            ("]}", 221),
        ]
        for k, v in _py_simple:
            py_simple.append((k[0], v))
            py_simple.append((k[-1], (shift, v)))

        punctuation_keys = py_special + py_simple
        self._meta_.update(dict(punctuation_keys))

    @property
    def meta(self):
        return self._meta_


class Mouse(object):
    def __init__(self, handle=None):
        self.handle = handle

    def click(self, pos, delay=0.25, double=False):
        if double:
            for i in range(2):
                self._click(pos)
        else:
            self._click(pos)

        time.sleep(delay)
        return 0

    def move(self, pos):
        self._move(pos)

    def abs_click(self, args, delay=0.25, double=False):
        print("abs_click, receive: ".ljust(30) + repr(args))

        if double:
            for i in range(2):
                self._abs_click(args)
        else:
            self._abs_click(args)

        time.sleep(delay)
        return 0

    @staticmethod
    def mouse2(args, double=False):
        x, y = args
        dx, dy = DisplaySize()
        print(x * 65536 / dx)
        print(y * 65536 / dy)

        if double:
            for i in range(2):
                mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x * 65536 / dx, y * 65536 / dy, 0, 0)
                mouse_event(win32con.MOUSEEVENTF_LEFTUP, x * 65536 / dx, y * 65536 / dy, 0, 0)
        else:
            mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x * 65536 / dx, y * 65536 / dy, 0, 0)
            mouse_event(win32con.MOUSEEVENTF_LEFTUP, x * 65536 / dx, y * 65536 / dy, 0, 0)

        return 0

    def _click(self, pos):
        assert self.handle is not None

        coordinate = win32api.MAKELONG(*pos)
        win32gui.SendMessage(self.handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        win32api.SendMessage(self.handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, coordinate)
        time.sleep(INTER_SLEEP)
        win32api.SendMessage(self.handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, coordinate)
        return 1

    @staticmethod
    def _abs_click(args):
        x, y = args
        win32api.SetCursorPos(args)
        mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        time.sleep(INTER_SLEEP)
        mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        return 1

    def _move(self, pos):
        assert self.handle is not None

        mv = win32gui.ClientToScreen(self.handle, pos)
        win32api.SetCursorPos(mv)

        return 1


class Keyboard(object):
    def __init__(self, handle=None):
        self.handle = handle

    def press(self, char, delay=0.25):
        print("press, receive: ".ljust(30) + repr(char))

        for c in char:
            code = key_map[c]

            if isinstance(code, tuple):
                self.comb_press_by_chr(code, delay=delay)
            else:
                self._press(code)

            time.sleep(delay)
        return 0

    def press_by_chr(self, char, delay=0.25):
        assert isinstance(char, (int, list))
        print("press, receive: ".ljust(30) + repr(char))

        if isinstance(char, list):
            for c in char:
                self._press(c)
                time.sleep(delay)
        else:
            self._press(char)
        return 0

    def comb_press(self, args, delay=0.25):
        print("comb_press, receive: ".ljust(30) + repr(args))

        func_key, extra_key = args[0], args[1]
        if extra_key.isupper():
            print("Error [in function comb_press]: It should be LowerCase. And now has been auto cover.")

        func_key, extra_key = key_map[args[0]], key_map[extra_key.lower()]
        self._comb_press((func_key, extra_key))
        time.sleep(delay)
        return 0

    def comb_press_by_chr(self, args, delay=0.25):
        print("comb_press_by_chr, receive: ".ljust(30) + repr(args))

        self._comb_press(args)
        time.sleep(delay)
        return 0

    def clear(self):
        self.comb_press(("Control", "a"))
        self.press_by_chr(key_map["Delete"])

    @staticmethod
    def _press(char):
        keybd_event(char, 0, 0, 0)
        keybd_event(char, 0, win32con.KEYEVENTF_KEYUP, 0)

        # time.sleep(INTER_SLEEP)
        Keyboard.check_key_state(char)

        return 1

    @staticmethod
    def _comb_press(chars):
        func_key, extra_key = chars

        keybd_event(func_key, 0, 0, 0)
        keybd_event(extra_key, 0, 0, 0)
        keybd_event(extra_key, 0, win32con.KEYEVENTF_KEYUP, 0)
        keybd_event(func_key, 0, win32con.KEYEVENTF_KEYUP, 0)

        # time.sleep(INTER_SLEEP)
        Keyboard.check_key_state(chars)

        return 1

    @staticmethod
    def check_key_state(args):
        keys = isinstance(args, int) and [args] or args

        for release_key in keys:
            if win32api.GetAsyncKeyState(release_key) < 0:
                keybd_event(release_key, 0, win32con.KEYEVENTF_KEYUP, 0)


class PS2(object):
    def __init__(self, handle=None):
        self.mouse = Mouse(handle)
        self.keyboard = Keyboard(handle)


def get_windows(wnm, do_more=False, delay=1):
    hwnd = win32gui.FindWindow(*wnm)
    if not hwnd:
        raise WindowsError(win32api.MessageBox(0, u"找不到窗口: %s" % wnm[1], u"警告", win32con.MB_ICONWARNING))

    print(hwnd)
    if do_more:
        print("do_more: " + repr(do_more))
        # win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 强行显示界面
        win32gui.SetForegroundWindow(hwnd)  # 将浏览器窗口提到前台
        time.sleep(delay)

    return hwnd


class WeChat(object):
    def __init__(self, title=('Qt5QWindowIcon', u"Android Emulator - weixin:5554"), do_more=True, delay=1.25):
        self.hwnd = win32gui.FindWindow(*title)
        if not self.hwnd:
            raise WindowsError(win32api.MessageBox(0, u"找不到窗口: %s" % wnm[1], u"警告", win32con.MB_ICONWARNING))

        if do_more:
            print("do_more: " + repr(do_more))
            # win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 强行显示界面
            win32gui.SetForegroundWindow(self.hwnd)  # 将浏览器窗口提到前台
            time.sleep(delay)

        self.ps2 = PS2(handle=self.hwnd)
        self.abs_z, self.abs_s, self.abs_y, self.abs_x = win32gui.GetWindowRect(self.hwnd)  # 实际使用abs_z, abs_s
        print(self.hwnd)

    def capture_client(self):
        img = ImageGrab.grab(bbox=(self.abs_z, self.abs_s, self.abs_y, self.abs_x))

        return img

    def _pick_color(self, box):
        assert isinstance(box, (tuple, list))

        client_img = self.capture_client()
        if isinstance(box, list):
            pick_area = [(client_img.crop(b), b) for b in box]
        else:
            pick_area = (client_img.crop(box), box)

        return pick_area

    def pick_add_button(self):
        evl = lambda x, y: (x, y) + (x + 1, y + 1)
        box = [evl(120, i) for i in range(480, 700, 10)]
        result = self._pick_color(box=box)

        rv_and_pos = {i.tobytes().encode("hex"): v[:2] for i, v in result}
        print(rv_and_pos)
        return rv_and_pos

    def click_search_box(self, clear=False, delay=0.25):
        u"""点击搜索框"""
        self.ps2.mouse.abs_click((self.abs_z + 145, 140), delay=delay)
        if clear:
            self.ps2.mouse.abs_click((self.abs_z + 470, 140), delay=delay)

    def click_search_and_result(self, delay=0):
        u"""点击搜索及搜索的第一条结果"""
        self.ps2.mouse.abs_click((self.abs_z + 120, 200), delay=delay)

    def handle_error_search(self, delay=0):
        u"""处理不存在的搜索"""
        self.click_search_box(delay=delay)

    def click_back_button(self, delay=0.5):
        u"""点击返回按钮"""
        self.ps2.mouse.abs_click((self.abs_z + 90, 150), delay=delay)

    def click_add_button(self, args, delay=1.5):
        u"""点击添加(好友)按钮"""
        x, y = args
        print(args)
        self.ps2.mouse.abs_click((self.abs_z + x, y), delay=delay)

    def click_send_button(self, delay=0):
        u"""点击发送申请(好友)按钮"""
        self.ps2.mouse.abs_click((self.abs_z + 450, 150), delay=delay)


def wx_add_friend(client, wx_name):
    # edit delay
    exist = 0
    wx_client = client
    wx_client.click_search_box()
    wx_client.ps2.keyboard.press(wx_name)

    time.sleep(0.8)
    wx_client.click_search_and_result(delay=14)  # click for search
    set_time = time.time()
    # wx_client.click_search_and_result(delay=3)  # click for result

    while True:
        rv_and_pos = wx_client.pick_add_button()
        add_pos = rv_and_pos.get("efebef")
        if add_pos:
            wx_client.click_add_button(add_pos, delay=12)
            wx_client.click_send_button(delay=10)
            wx_client.click_back_button(delay=8)
            exist = 1
            break

        if time.time() > set_time + 3:
            wx_client.handle_error_search(delay=8)
            break

        time.sleep(CUT_SLEEP)  # 截图间隔

    wx_client.click_search_box(clear=True)

    print("wx_add_friend, result: ".ljust(30) + ", ".join([repr(exist), wx_name]))


if __name__ == '__main__':
    key_map = KeyMap().meta
    wxClient = WeChat()

    with open(r"C:\Users\android\Desktop\mingdan.txt") as rf:
        data = rf.readlines()

        for zh in data:
            wx_hao = zh.strip()

            wx_add_friend(wxClient, wx_hao)

            time.sleep(10)
