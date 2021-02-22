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

import hashlib
import pickle
import time


class memoize(object):
    '''
    缓存类, 缓存函数的执行结果，类中的方法不建议加
    '''

    def __init__(self, duration=None, is_log=False):
        '''
        如果没有加时间，表示程序生命周期内一直保存，对于全生命周期的结果可以这样做
        :param duration: 缓存时间
        :param is_log: 是否打印日志，如果是类中函数建议不打印日志，如果频繁调用也不建议打印日志
        '''
        self.__cache = {}
        self.__duration = duration
        self.__is_log = is_log

    def __call__(self, func):
        def __memorize(*args, **kwargs):
            key = self.__compute_key(func, args, kwargs)
            if key in self.__cache and not self.__is_obsolete(self.__cache[key]):
                if self.__is_log:
                    print('fit the cache of function: {}, with args: {} and kwargs: {}'.format(func.__name__,
                                                                                               args,
                                                                                               kwargs))
                # 如果缓存中有，就直接返回缓存过的结果
                return self.__cache[key]['value']
            result = func(*args, **kwargs)
            self.__cache[key] = {'value': result, 'time': time.time()}

            return result

        return __memorize

    def __is_obsolete(self, entry):
        '''
        判断缓存是否过期，返回True则过期
        :param entry:
        :param duration:
        :return:
        '''
        if self.__duration is None:
            return False
        diff = time.time() - entry['time']

        return diff > self.__duration

    def __compute_key(self, function, args, kwargs):
        '''
        将传入的参数序列化
        :param function:
        :param args:
        :param kwargs:
        :return:
        '''
        # 实例方法中使用时，实例对象会作为args[0] 传递过来
        key = pickle.dumps((function.__name__, args, kwargs))
        return hashlib.sha1(key).hexdigest()
