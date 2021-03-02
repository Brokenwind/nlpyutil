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

import inspect
import logging
import os
import sys
import time
from functools import wraps
from . import Singleton


def _append_log_info(func):
    '''
    为日志信息添加更详细的信息
    :param func:
    :return:
    '''
    _append_format = ' {} - {} - {}'

    @wraps(func)
    def append(call_object, msg, *args, **kwargs):
        '''
        :param call_object: 调用对象的引用
        :param msg: 日志信息
        :param args:
        :param kwargs:
        :return:
        '''
        # 获取调用者的信息
        stack = inspect.stack()
        if len(stack) >= 2:
            frame, filename, line_number, function_name, lines, index = stack[1]
        else:
            line_number = "unknown"
            function_name = "unknown"
        message = _append_format.format(function_name, line_number, msg)
        func(call_object, message, **kwargs)

    return append

@Singleton
class Logger:
    '''
    如需打印不同路径的日志（运行日志、审计日志），则不能使用单例模式（注释或删除此行）。此外，还需设定参数name。
    '''

    def __init__(self, set_level='debug',
                 name=os.path.split(os.path.splitext(sys.argv[0])[0])[-1],
                 log_name=time.strftime("%Y-%m-%d-%H.log", time.localtime()),
                 log_path=None,
                 use_console=True):
        """
        :param set_level: 日志级别["NOTSET"|"DEBUG"|"INFO"|"WARNING"|"ERROR"|"CRITICAL"]，默认为INFO
        :param name: 日志中打印的name，默认为运行程序的name
        :param log_name: 日志文件的名字，默认为当前时间（年-月-日.log）
        :param log_path: 日志文件夹的路径，默认为logger.py同级目录中的log文件夹
        :param use_console: 是否在控制台打印，默认为True
        """
        if not set_level:
            # 设置set_level为None，自动获取当前运行模式
            set_level = self._exec_type()
        self.__logger = logging.getLogger(name)
        self.logger.setLevel(
            # 设置日志级别
            getattr(logging, set_level.upper()) if hasattr(logging, set_level.upper()) else logging.INFO)
        # 创建日志目录
        if log_path and not os.path.exists(log_path):
            os.makedirs(log_path)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler_list = list()
        if log_path:
            handler_list.append(logging.FileHandler(os.path.join(log_path, log_name), encoding="utf-8"))
        if use_console:
            handler_list.append(logging.StreamHandler())
        for handler in handler_list:
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    '''
    # 此处无法和Parallel 一起使用
    # 当调用不存在的属性时，会试图调用__getattr__(self,'key')来获取属性
    def __getattr__(self, item):
        return getattr(self.logger, item)
    '''

    @_append_log_info
    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    @_append_log_info
    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    @_append_log_info
    def warn(self, msg, *args, **kwargs):
        self.logger.warn(msg, *args, **kwargs)

    @_append_log_info
    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    @property
    def logger(self):
        return self.__logger

    @logger.setter
    def logger(self, func):
        self.__logger = func

    def _exec_type(self):
        return "DEBUG" if os.environ.get("IPYTHONENABLE") else "INFO"
