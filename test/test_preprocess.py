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

from nlpyutil.preprocess import *


def test_process():
    pipe = PreprocessPipeline(
        func_list=[
            preprocess_remove_not_chinese,
            preprocess_text_to_simple,
            preprocess_text_to_dbc])
    print(pipe.process([' kǒu yīn  kəmˈpjutɚ,臺灣是位於東亞、it is great太平洋西北側的島嶼NOCE',
                        ' kǒu yīn  kəmˈpjutɚ, https://www.baidu.com,wangkun@eversec.com']))
    '''
    print(preprocess_split_on_punc('哈哈哈，真是个好天气，yes!!'))
    print(preprocess_remove_not_chinese('哈哈哈，真是个好天气，yes!!,https://www.baidu.com,wangkun@eversec.com'))

    print(preprocess_remove_duplacte_words('東亞亞亞、、、it----.... is'))
    print(preprocess_remove_symbols(
        'yes$█▄▇▆▅▃▅▄▃▃▃▃▅▇▄▄▄▃▃▃▃▇█▇▆▅▅▅▄▅▆▃▃▃▃▃▃▃▆▇▆▅▆▆▅▄▅▄▃▃▃▂▂▂▂▄▇▅▄▆▄▅▄▄▃▂▂▂▂▂▂▂▄▇▆▅▆▄▄▄▃▂▂▂▂▂▂▂▂▆▆▆▆▄▄▄▃▂▂▂▂▁▁▁▁▁▆▇▆▅▄▃▄▁▁▁▁▁▃▇██▆▆▇▆▅▃▅█████▄▃▅▁▅██▆▃███████▅▄▇▄▅█████'))
    print(preprocess_remove_not_chinese(
        "中共も「左翼」、アメリカも「左翼」になっちまうのかねえ？日本の「左翼」は困るですなあ。つまり21世紀の左翼とはつまり民族主義のことかいな？ https://t.co/9KIML9zJuw//暇爺 :趣味はバイクと猫と何・程両氏の大雑把翻訳。@Minya_J:何清漣氏★米国民主党のバイデンという選択"))

    # print(preprocess_text_segmentation("麻豆传媒映画品牌大使迪丽热巴 →网页链接←", seg_method='jieba'))
    '''


if __name__ == '__main__':
    test_process()
