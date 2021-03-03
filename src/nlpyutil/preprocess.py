# -*- coding: utf-8 -*-#
# Time:         3/6/2020
# Author:       WangKun
# Email:        wangkun6536@163.com
# Desc:         公用的一些预处理方法

import re
import string
from collections import Iterable
from functools import wraps

import jieba
import langdetect
import unicodedata
from opencc import OpenCC

from . import ch_utils
from . import rarewords
from . import stopwords
from . import usual_pattern

_STOP_WORDS = stopwords.STOPWORDS
_STOP_WORDS.extend(rarewords.RAREWORDS)
# set 有助于提升速度
_STOP_WORDS = set(_STOP_WORDS)
_RARE_WORDS = set(rarewords.RAREWORDS)
_t2s = OpenCC('t2s')


def process_iter(func):
    """
    为预处理函数处理当参数是list的情况
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(data, **kwargs):
        if not data:
            return data
        elif isinstance(data, str):
            return func(data, **kwargs)
        elif isinstance(data, Iterable):
            process_res = []
            for text in data:
                processed_text = func(str(text), **kwargs)
                process_res.append(processed_text)
            return process_res
        else:
            raise ValueError('parameter:{} can not convert_pipeline'.format(type(data)))

    return wrapper


class PreprocessPipeline(object):
    """
    数据预处理pipeline
    使用此pipeline时的注意事项：
      1. func_list 中添加的函数第一个参数是需要处理的数据，其它参数必须是key=value，也就是**kwargs
      2. func_list 中添加的函数输出输出据必须要和输入数据格式，类型相同
    """

    def __init__(self, func_list, **kwargs):
        '''
        :param func_list: 函数列表
        :param kwargs: 函数列表中函数所需要的参数
        '''
        self._func_list = func_list
        self._check_params()
        self._kwargs = kwargs

    def _check_params(self):
        pass

    def process(self, data):
        for func in self._func_list:
            data = func(data, **self._kwargs)
        return data


def get_stopwords():
    return _STOP_WORDS


@process_iter
def preprocess_remove_not_chinese(data: str, **kwargs):
    '''
    移除非中文字符
    :param data:
    :param kwargs 吸收不相关参数
    :return:
    '''
    return ''.join(usual_pattern.PATTERN_CHINESE_CHARS.findall(data))


@process_iter
def preprocess_remove_en_chars(data: str, **kwargs):
    '''
    去除英文字符
    :param text:
    :return:
    '''
    return ''.join(filter(lambda x: x not in string.printable, data))


@process_iter
def preprocess_strip_blanks(data: str, **kwargs):
    '''
    消除句子中的空格
    :param data:
    :param kwargs:
    :return:
    '''
    return re.sub(usual_pattern.PATTERN_SPACES, '', data)


@process_iter
def preprocess_remove_links(data: str, **kwargs):
    '''
    删除句子中的链接，包括邮件，ftp，http等协议的链接
    :param data:
    :param kwargs:
    :return:
    '''
    data = re.sub(usual_pattern.PATTERN_EMAIL, '', data)
    data = re.sub(usual_pattern.PATTERN_URL, '', data)

    return data


@process_iter
def preprocess_text_to_dbc(data: str, **kwargs):
    '''
    全角转半角
    :param kwargs 吸收不相关参数
    :return:
    '''
    return ch_utils.str_to_dbc(data)


@process_iter
def preprocess_text_to_simple(data: str, **kwargs):
    '''
    数据繁体转简体
    :param data:
    :param kwargs 吸收不相关参数
    :return:
    '''
    return _t2s.convert(data)


@process_iter
def preprocess_text_to_lower(data: str, **kwargs):
    return data.lower()


@process_iter
def preprocess_strip_accents(data: str, **kwargs):
    """
    去除重音符号，类似于拼音的音调
    :param data:
    :param kwargs: 吸收不相关参数
    :return:
    """
    data = unicodedata.normalize("NFD", data)
    output = []
    for char in data:
        cat = unicodedata.category(char)
        if cat == "Mn":
            continue
        output.append(char)
    return "".join(output)


@process_iter
def preprocess_split_on_punc(data: str, **kwargs):
    """
    根据标点符号对句子进行切分
    :param data:
    :param kwargs:
    :return:
    """

    def _is_punctuation(char):
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

    res_tokens = []
    for char in data:
        if _is_punctuation(char):
            res_tokens.append(" ")
        else:
            res_tokens.append(char)
    res_str = ''.join(res_tokens)

    return res_str


@process_iter
def preprocess_text_segmentation(data: str,
                                 joint=' ',
                                 remove_stopwords=True,
                                 remove_punc=True,
                                 remove_rare=True,
                                 **kwargs):
    '''
    句子分词
    :param data:
    :param joint: 分词后的连接字符
    :param user_dict:  用户自定义分词词典，注意，此处已经默认加载了kps分类配置种的关键词
    :param remove_stopwords: 是否移除停用词
    :param remove_punc: 是否移除标点符号
    :param remove_rare: 是否移除都是生僻字的词
    :param kwargs 吸收不相关参数
    :return:
    '''
    # ltp的自定义词典会不生效
    terms = jieba.cut(data)
    if remove_stopwords:
        terms = [term for term in terms if term not in _STOP_WORDS]

    filterd_terms = []

    for idx, term in enumerate(terms):
        if remove_rare:
            is_rare = all([chr in _RARE_WORDS for chr in term])
            if is_rare:
                continue
        if remove_punc:
            chrs = [chr for chr in term if not ch_utils.is_punctuation(chr)]
            new_term = ''.join(chrs)
            new_term = new_term.strip()
        else:
            new_term = term
        if new_term:
            filterd_terms.append(new_term)

    return joint.join(filterd_terms)


@process_iter
def preprocess_replace_whitespace(data: str, repl=' ', **kwargs):
    """
    将所有的空白符替换为指定符号
    :param data:
    :return:
    """
    return re.sub(usual_pattern.PATTERN_WHITE_SPACE, repl, data)


@process_iter
def preprocess_remove_html_marks(data: str, **kwargs):
    """
    移除html标签
    :param data:
    :param kwargs:
    :return:
    """
    return usual_pattern.PATTERN_HTML_MAKR.sub('', data)


@process_iter
def preprocess_replace_html_marks(data: str, object="，", **kwargs):
    """
    移除html标签
    :param data:
    :param kwargs:
    :return:
    """
    return usual_pattern.PATTERN_HTML_MAKR.sub(object, data)


@process_iter
def preprocess_remove_duplacte_words(data, **kwargs):
    """
    去除很多重复的词和标点符号
    preprocess_remove_duplacte_words('東亞亞亞、、、it----.... is')

    東亞、it-. is
    """
    reg = r'([^0-9I]+)(\1){2,}'
    for i in range(6):
        temp = data
        data = re.sub(reg, lambda m: m.group(1), data)
        if len(data) == len(temp):
            break
    return data


def preprocess_remove_symbols(data: str, **kwargs):
    """
    移除不知名的特殊符号
    :param data:
    :param kwargs:
    :return:
    """
    data_res = []
    for chr in data:
        cate = unicodedata.category(chr)
        # Symbol, Other; Symbol, Currency
        if cate == 'So' or cate == 'Sc':
            continue
        data_res.append(chr)

    return ''.join(data_res)


@process_iter
def preprocess_filter_other_language(data: str, **kwargs):
    """
    过滤掉非中文文本，当文本为非中文时，直接返回空字符串
    :param data:
    :param kwargs:
    :return:
    """
    try:
        lag = langdetect.detect(data)
    except Exception as e:
        return ""
    if lag == 'zh-cn':
        return data
    else:
        return ""


@process_iter
def preprocess_weibo_content(data: str, sentence_joint_chr='，', **kwargs):
    """
    处理微博内容
    :param line:
    :return:
    """
    topics = re.findall(usual_pattern.WEIBO_PATTERN_TOPIC, data)
    topic = sentence_joint_chr.join(topics)
    if len(topic) < 15:
        data = re.sub(usual_pattern.PATTERN_URL, sentence_joint_chr, data)
        if data.endswith("...全文"):
            data = data[:len(data) - 6]
        items = []
        if topic:
            items.append(topic)
        for item in data.split("//"):
            # 去除@的人物
            item = re.sub(r'@.{1,15}[:：\ ]', '', item)
            if not item:
                continue
            items.append(item)
        result = sentence_joint_chr.join(items)
    else:
        result = topic

    return result
