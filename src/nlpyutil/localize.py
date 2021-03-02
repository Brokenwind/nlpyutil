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

import json
import threading

import pandas as pd


class LocalizeThread(threading.Thread):
    '''
    数据本地化线程
    '''

    def __init__(self, data, file_path, columns=[], sep='\t'):
        '''
        :param data: 需要本地化的数据
        :param file_path: 本地化的文件名及其路径
        '''
        threading.Thread.__init__(self)
        self.data = data
        self.file_path = file_path
        self.columns = columns
        self.sep = sep

    def run(self):
        if isinstance(self.data, pd.DataFrame) or isinstance(self.data, pd.Series):
            # DataFrame 或者Series直接调用其to_csv方法
            if self.columns:
                self.data.to_csv(self.file_path, encoding="utf-8", index=False, sep=self.sep, columns=self.columns)
            else:
                self.data.to_csv(self.file_path, encoding="utf-8", index=False, sep=self.sep, header=None)
        elif isinstance(self.data, dict) or isinstance(self.data, list):
            # dict 获取 list进行json化
            data_str = json.dumps(self.data, indent=4, ensure_ascii=False)
            self._localize_data(data_str, self.file_path)
        else:
            data_str = str(self.data)
            self._localize_data(data_str, self.file_path)

    def _localize_data(self, data: str, file_path):
        '''
        本地化数据
        :param data: 需要保存的数据
        :param file_path: 保存的路径
        :return:
        '''
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(data)
