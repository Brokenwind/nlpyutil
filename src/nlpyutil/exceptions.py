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

"""
Exceptions that may happen in the project.
"""


class UserBaseException(Exception):
    '''
    本项目中所有异常类的父类
    '''

    def __init__(self, message, code=None):
        super().__init__(message)
        self.message = message
        self.code = code


class ParameterException(UserBaseException):
    '''
    参数错误时抛出
    '''

    def __init__(self, message='parameter error', code=501):
        super().__init__(message, code)


class CalculationException(UserBaseException):
    '''
    在计算时出现问题抛出异常
    '''

    def __init__(self, message='calculation error', code=502):
        super().__init__(message, code)


class ValueException(UserBaseException):
    '''
    值出现问题时抛出异常
    '''

    def __init__(self, message='value error', code=503):
        super().__init__(message, code)
