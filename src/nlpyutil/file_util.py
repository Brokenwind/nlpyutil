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

import os
import psutil
import platform


def is_windows_ready(path):
    """
    windows下的文件是否已经准备好
    :param path:
    :return:
    """
    try:
        with open(path, 'r'):
            ready = True
    except Exception:
        ready = False
    return ready


def is_linux_ready(path):
    """
    linux下的文件是否已经准备好
    :param path:
    :return:
    """
    for proc in psutil.process_iter():
        try:
            for item in proc.open_files():
                if path == item.path:
                    return False
        except Exception:
            pass

    return True


def is_ready(path):
    """
    文件是否准备就绪
    :param path:
    :return:
    """
    if (platform.system() == 'Windows'):
        return is_windows_ready(path)
    elif (platform.system() == 'Linux'):
        return is_linux_ready(path)
    else:
        return is_linux_ready(path)


def get_ready_files(dir):
    """
    获取目录下已经准备好的文件
    :param dir:
    :return:
    """
    files = []
    for name in os.listdir(dir):
        filepath = os.path.join(dir, name)
        if os.path.isdir(filepath):
            continue
        if is_ready(filepath):
            files.append(filepath)

    return files
