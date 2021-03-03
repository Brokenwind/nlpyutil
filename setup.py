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

from setuptools import find_packages, setup

_deps = [
    "numpy>=1.17",
    "dataclasses",
    "zhon",
    "langdetect",
    "opencc-python-reimplemented",
    "jieba"
]

# some of the values are versioned whereas others aren't.
deps = {b: a for a, b in (re.findall(r"^(([^!=<>]+)(?:[!=<>].*)?$)", x)[0] for x in _deps)}

# when modifying the following list, make sure to update src/transformers/dependency_versions_check.py
install_requires = [
    deps["numpy"],
    deps["dataclasses"] + ";python_version<'3.7'",  # dataclasses for Python versions that don't have it
    deps["zhon"],
    deps["langdetect"],
    deps["opencc-python-reimplemented"],
    deps["jieba"]
]

setup(name='nlpyutil',
      version='0.4.0',
      description='Personal usual utils for python',
      long_description=open("README.md", "r", encoding="utf-8").read(),
      long_description_content_type="text/markdown",
      author='kun, wang',
      author_email='wangkun6536@gmail.com',
      url='https://github.com/Brokenwind/nlpyutil',
      license="MIT",
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Natural Language :: Chinese (Traditional)',
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          'Topic :: Text Processing',
          'Topic :: Text Processing :: Indexing',
          'Topic :: Text Processing :: Linguistic',
      ],
      keywords='NLP, Utils',
      packages=find_packages("src"),
      package_dir={"": "src"},
      package_data={'nlpyutil': ['data/rarewords.txt']},
      install_requires=install_requires
      )
