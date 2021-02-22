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
from zhon import hanzi
import string

# 中文标点符号
DATA_CHINESE_PUNCTUATION = list(hanzi.punctuation)
# 英文标点符号
DATA_ENGLISH_PUNCTUATION = list(string.punctuation)
# 中英文标点符号
DATA_CHINESE_ENGLISH_PUNCTUATION = DATA_CHINESE_PUNCTUATION + DATA_ENGLISH_PUNCTUATION

PATTERN_SPACES = re.compile(r'( |\t)+')
# 中文字符，包括汉字和中文标点符号两部分
PATTERN_CHINESE_CHARS = re.compile(
    r'[\u4e00-\u9fa5]+' + '|[' + ''.join(DATA_CHINESE_PUNCTUATION + [',', '!']) + ']+')
# 邮件地址
PATTERN_EMAIL = re.compile(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)+')
# 完整URL
PATTERN_URL = re.compile(
    r'(?:[a-zA-Z]+://)*(?:[a-zA-Z_-]+(?:\.[0-9a-zA-Z]+)[a-zA-Z0-9 %_@/$.&+?=-]*)')
# 数字提取
PATTERN_NUMBER = r'[1-9]+\.?[0-9]*'
# 身份证
PATTERN_ID_CARD = re.compile(r'[1-9]\\d{16}[a-zA-Z0-9]{1}')
# 手机: 验证手机号码（支持国际格式，+86135xxxx...（中国内地），+00852137xxxx...（中国香港））
PATTERN_MOBILE = re.compile(r'(?:\D|^)((?:\+\d+)?1[3458]\d{9})(?:\D|$)')
# 电话: 国家（地区）电话代码 + 区号（城市代码） + 电话号码，如：+8602085588447
# TODO:  (目前有问题)
PATTERN_PHONE = re.compile(r'(?:\D|^)((?:\+\d+)?(?:\d{3,4}\-?)?\d{7,8})(?:\D|$)')
# 文章中的html标签正则表达式
PATTERN_HTML_MAKR = re.compile(r'<[^>]+>', re.S)
# 某些unicode编码范围的也认为是空格
PATTERN_WHITE_SPACE = r'[\u2000-\u2010]+|\s+'
# 微博相关
WEIBO_PATTERN_USER = re.compile(r'@[\\u4e00-\\u9fa5\\w\\-]+')
WEIBO_PATTERN_TOPIC = re.compile(r'#([^#]+)#')
# 传统相关需要处理的
CHUANTONG_BOOK_MARK = re.compile(r'【.{0,20}】')
CHUANTONG_SENTENCE_SPLITTER = re.compile(r'[\u3000]+')


def extract_emails(text: str):
    """
    提取文本中的邮件
    :param text:
    :return:
    """
    emails = re.findall(PATTERN_EMAIL, text)
    if emails:
        return '|'.join(emails)
    else:
        return None


def extract_urls(text: str):
    '''
    获取文档中的url链接
    :param text:
    :return:
    '''
    urls = []
    http_urls = re.findall(PATTERN_URL, text)
    if http_urls:
        urls.extend(http_urls)
    if urls:
        return '|'.join(list(set(urls)))
    else:
        return None


def extract_phones(text: str):
    """
    抽取电话号码
    :param text:
    :return:
    """
    result = []
    mobiles = re.findall(PATTERN_MOBILE, text)
    if mobiles:
        result.extend(mobiles)
    '''
    phones = re.findall(PATTERN_PHONE, text)
    if phones:
        #print(phones)
        result.extend(phones)
    '''
    result = list(set(result))
    return "|".join(result)


def remove_unusual_ch_marks(text: str, replace_with=' '):
    '''
    去除中文中不常用标点
    :param text:
    :param replace_with: 被去除的符号的代替符号
    :return:
    '''
    DATA_UNUSUAL_CHINESE_MARK = ['–', '—', '‘', '’', '“', '”', '…', '〈', '〉', '《', '》', '「', '」',
                                 '『', '』', '【', '】',
                                 '〔', '〕', '（', '）']
    pattern = "|".join(DATA_UNUSUAL_CHINESE_MARK)

    return re.sub(pattern, replace_with, text)


if __name__ == '__main__':
    print(r'[\u4e00-\u9fa5]+' + '|[' + ''.join(DATA_CHINESE_ENGLISH_PUNCTUATION) + ']')
    print(extract_phones(
        '【朵拉高质洗衣】您的1件衣物已收妥，单号1538370，待结算。18554339081 详http://t.cn/Etzl0I7 http://t.cn/Etzl0I7'))
    print(extract_urls(
        '【朵拉高质洗衣】您的1件衣物已收妥，单号1538370，待结算。18554339081 详https://www.t.cn/Etzl0I7'))
    print(re.findall(PATTERN_URL,
                     ';123@163.com.非常好'))
