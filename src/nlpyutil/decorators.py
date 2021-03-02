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

from functools import wraps


def deprecated(func):
    '''
    主要用于标记函数过期不可用
    :param func:
    :return:
    '''

    @wraps(func)
    def _wrapper(*args, **kwargs):
        print('The function {} is deprecated, it will be removed in future version'.format(func.__name__))
        return func(*args, **kwargs)

    return _wrapper


def disabled(func):
    '''
    主要标记函数不可用
    :param func:
    :return:
    '''

    @wraps(func)
    def _wrapper(*args, **kwargs):
        print('The function {} is disabled, it is not allowed to access'.format(func.__name__))
        raise RuntimeError('the function {} is disabled.'.format(format(func.__name__)))

    return _wrapper


def override(func):
    '''
    主要标记函数重写父类方法
    :param func:
    :return:
    '''

    @wraps(func)
    def _wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return _wrapper
