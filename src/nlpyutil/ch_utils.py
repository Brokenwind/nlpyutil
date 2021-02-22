# -*- coding: utf-8 -*-
# MIT License

# Copyright (c) 2021 Brokenwind

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
import six
import unicodedata
from nlpyutil import usual_pattern


def convert_to_unicode(text):
    """在默认字符编码为utf-8的前提下，将文本转换为unicode"""
    if six.PY3:
        if isinstance(text, str):
            return text
        elif isinstance(text, bytes):
            return text.decode("utf-8", "ignore")
        else:
            raise ValueError("Unsupported string type: %s".format(type(text)))
    elif six.PY2:
        if isinstance(text, str):
            return text.decode("utf-8", "ignore")
        elif isinstance(text, unicode):
            return text
        else:
            raise ValueError("Unsupported string type: %s".format(type(text)))
    else:
        raise ValueError("Not running on Python2 or Python 3?")


def printable_text(text):
    if six.PY3:
        if isinstance(text, str):
            return text
        elif isinstance(text, bytes):
            return text.decode("utf-8", "ignore")
        else:
            raise ValueError("Unsupported string type: %s".format(type(text)))
    elif six.PY2:
        if isinstance(text, str):
            return text
        elif isinstance(text, unicode):
            return text.encode("utf-8")
        else:
            raise ValueError("Unsupported string type: %s".format(type(text)))
    else:
        raise ValueError("Not running on Python2 or Python 3?")


def str_to_dbc(ustring):
    '''
    把字符串全角转半角
    :param ustring:
    :return:
    '''
    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            # 全角空格直接转换
            if inside_code == 12288:
                inside_code = 32
            # 全角字符（除空格）根据关系转化
            elif (inside_code >= 65281 and inside_code <= 65374):
                inside_code -= 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)


def str_to_sbc(ustring):
    '''
    把字符串全角转半角
    :param ustring:
    :return:
    '''
    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            # 全角空格直接转换
            if inside_code == 32:
                inside_code = 12288
            # 全角字符（除空格）根据关系转化
            elif (inside_code >= 33 and inside_code <= 126):
                inside_code += 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)


def is_whitespace(char):
    """判断字符是否是空白符"""
    if re.match(usual_pattern.PATTERN_WHITE_SPACE, char):
        return True
    # 有些字符技术上是控制字符，但实际使用中将其对待为空白符
    if char == " " or char == "\t" or char == "\n" or char == "\r":
        return True
    cat = unicodedata.category(char)
    if cat == "Zs" or cat == "Cf":
        return True
    return False


def is_visiable_ascii(char):
    '''
    是否是可见ascii码
    :param char:
    :return:
    '''
    return 32 <= ord(char) and ord(char) < 127


def is_punctuation(char):
    """检查一个字符是否是标点符号"""
    cp = ord(char)
    #  ASCII码中，不是数字和字母外的其它字符都算作标点符号
    if ((cp >= 33 and cp <= 47) or (cp >= 58 and cp <= 64) or
            (cp >= 91 and cp <= 96) or (cp >= 123 and cp <= 126)):
        return True
    # unicode编码中其它的标点符号
    cat = unicodedata.category(char)
    if cat.startswith("P"):
        return True
    return False


if __name__ == '__main__':
    a = str_to_sbc("你好python")
    print(a)
    b = str_to_dbc(a)
    print(b)
    print(is_whitespace(chr(8205)))
    print(is_visiable_ascii('A'))
