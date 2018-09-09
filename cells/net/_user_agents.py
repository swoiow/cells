#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools


def exec_doc(f):
    @functools.wraps(f)
    def swap(*args, **kwargs):
        doc = (c.strip() for c in f.__doc__.split("\n") if c.strip())
        for line in doc:
            yield line

    return swap


@exec_doc
def _spider():
    """
    Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)
    Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)
    Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 (KHTML, like Gecko; Google Page Speed Insights) Chrome/22.0.1229 Safari/537.4 GoogleBot/2.1
    Sogou web spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)
    Mozilla/5.0 (compatible; Googlebot/2.1 +http://www.googlebot.com/bot.html)
    Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)
    msnbot/1.0 (+http://search.msn.com/msnbot.htm)
    Mozilla/5.0 (compatible; YoudaoBot/1.0; http://www.youdao.com/help/webmaster/spider/; )
    Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)
    Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)
    Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0); 360Spider
    Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36 QIHU 360SE; 360Spider
    """


@exec_doc
def _browser():
    """
    Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0)
    Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)
    Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)
    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML like Gecko) Version/9.0.2 Safari/601.3.9
    Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246
    Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586
    Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/64.0.3282.167 Safari/537.36
    Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko
    Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML like Gecko) Version/5.1.7 Safari/534.57.2
    Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0
    Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER
    Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/45.0.2454.101 Safari/537.36
    Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.3 Safari/537.36
    Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/47.0.2526.111 Safari/537.36
    Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.277.400 QBrowser/9.4.7658.400
    Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7
    Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/48.0.2564.116 UBrowser/5.6.12150.8 afari/537.36
    Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.32
    Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/50.0.2661.87 Safari/537.36
    Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Maxthon/4.9.2.1000 Chrome/39.0.2146.0 Safari/537.36
    Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1
    Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0
    Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.64 Safari/537.36
    Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1
    Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0
    Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/48.0
    Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/56.0
    Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36
    Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.78 Chrome/60.0.3112.78 Safari/537.36
    Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/57.0.2987.98 Chrome/57.0.2987.98 Safari/537.36
    Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11 QIHU 360EE
    Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; Zune 4.7; .NET4.0E; EIE10;ENUSWOL; QIHU 360EE)
    Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E; QIHU 360EE)
    Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MASM; .NET4.0C; .NET4.0E; QIHU 360EE)
    Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Trident/4.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.5.21022; InfoPath.2; CIBA; .NET CLR 3.5.30729; .NET4.0C; .NET CLR 3.0.30729; QIHU 360EE)
    Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; BRI/2; MAAR; .NET4.0C; .NET4.0E; InfoPath.3; QIHU 360EE)
    """


@exec_doc
def _mobile():
    """
    Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36
    Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36
    Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.10586
    Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MMB29P) AppleWebKit/537.36 (KHTML like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36
    Mozilla/5.0 (Linux; Android 6.0.1; E6653 Build/32.2.A.0.253) AppleWebKit/537.36 (KHTML like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36
    Mozilla/5.0 (Linux; Android 6.0; HTC One M9 Build/MRA58K) AppleWebKit/537.36 (KHTML like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36
    Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML like Gecko) Version/9.0 Mobile/13B143 Safari/601.1
    Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Tablet PC 2.0; InfoPath.3; .NET4.0C; .NET4.0E; QIHU 360EE)
    """
