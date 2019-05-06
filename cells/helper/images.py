#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid

from PIL import Image


def cut_pic2(fn, code='abcd', fp_label=None, saving=False):
    """ https://github.com/fate233/tensorflow-captcha-practice
    :param fn:
    :param code:
    :param fp_label:
    :param saving:
    :return:
    """

    import numpy as np

    im = Image.open(fn)
    w, h = im.size
    im = im.convert('L')
    im = im.point(lambda i: 0 if i < 120 else 255)
    y_buffer = []

    for x in range(im.size[0]):
        s = 0
        for y in range(im.size[1]):
            if im.getpixel((x, y)) < 125:
                s += 1

        y_buffer.append(s)

    y_sps = []
    b_in = False
    for x in range(w):
        if b_in and y_buffer[x] == 0:
            # out
            y_sps.append(x)
            b_in = False
        elif (not b_in) and y_buffer[x] > 0:
            # in
            y_sps.append(x - 1)
            b_in = True

    if len(y_sps) == 6:
        # 有一个交叠，找到最大的，中分
        max_p = 0
        max_c = -1
        for i in [0, 2, 4]:
            m = y_sps[i + 1] - y_sps[i]
            if m > max_c:
                max_c = m
                max_p = i

        md = int((y_sps[max_p + 1] - y_sps[max_p]) / 2)

        t = []
        t.extend(y_sps[:max_p])
        t.extend([y_sps[max_p], y_sps[max_p] + md, y_sps[max_p] + md + 1, y_sps[max_p + 1]])
        t.extend(y_sps[max_p + 2:])
        y_sps = t

    if len(y_sps) == 8:
        for x in y_sps:
            im.putpixel((x, 1), 125)

        ret = []
        for i, c in zip([0, 2, 4, 6], code):
            x_start = y_sps[i]
            x_end = y_sps[i + 1]
            crop = im.crop((x_start, 5, x_end, 45))
            image = Image.new('RGB', (40, 40), (255, 255, 255))
            image = image.convert('L')
            ww = x_end - x_start
            if ww > 40:
                print('error, dig to wide')
                ret = None
                break
            else:
                image.paste(crop, (int((40 - ww) / 2), 0, int((40 - ww) / 2) + ww, 40))
                fn_dig = 'yzm_dig/{}_{}.png'.format(c, uuid.uuid4())
                image.thumbnail((28, 28), Image.ANTIALIAS)
                ret.append(np.array(image, dtype=np.float32))
                if saving:
                    image.save(fn_dig)
                if fp_label:
                    image.save(fn_dig)
                    fp_label.write('{},{}\n'.format(fn_dig, c))
                    print((fn_dig, c))

        return ret
    else:
        print(('error img, ', fn))

    return None


def cut_pic(filename):
    """ https://security.yirendai.com/news/share/21
    图片处理（灰度化，二值化，切割图片）
    :param filename:
    :return:
    """

    filepath = filename
    im = Image.open(filepath)
    im_grey = im.convert('L')  # 灰度化
    # im_grey.show()

    # 二值化
    threshold = 130
    table = []
    cut = []
    real_cut = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    out = im_grey.point(table, '1')
    # out.show()

    # 分割图片
    width = out.width
    height = out.height
    # 取有像素0的列
    for x in range(0, width):
        for y in range(0, height):
            if out.getpixel((x, y)) == 0:
                cut.append(x)
                break
            else:
                continue

    # 保存要切割的列
    real_cut.append(cut[0] - 1)
    for i in range(0, len(cut) - 1):
        if cut[i + 1] - cut[i] > 1:
            real_cut.append(cut[i] + 1)
            real_cut.append(cut[i + 1] - 1)
        else:
            continue
    real_cut.append(cut[-1] + 1)

    # 切割图片
    count = [0, 2, 4, 6]
    child_img_list = []
    for i in count:
        child_img = out.crop((real_cut[i], 0, real_cut[i + 1], height))
        child_img_list.append(child_img)

    # 保存切割的图片
    # for i in range(0,4):
    # child_img_list[i].save("E:\%d.jpg" % i)

    # 横向切割
    cut_second = []
    final_img_list = []
    for i in range(0, 4):
        width = child_img_list[i].width
        height = child_img_list[i].height
        # 取有像素0的列
        for y in range(0, height):
            for x in range(0, width):
                if child_img_list[i].getpixel((x, y)) == 0:
                    cut_second.append(y)
                    break
                else:
                    continue
        # 切割图片
        final_img = child_img_list[i].crop((0, cut_second[0] - 1, width, cut_second[-1] + 1))
        final_img_list.append(final_img)
    # 返回切割的图片
    return final_img_list
