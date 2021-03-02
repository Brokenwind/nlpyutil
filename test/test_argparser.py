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

from nlpyutil import SdArgumentParser, string_to_bool
import argparse
import unittest
from argparse import Namespace
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


def list_field(default=None, metadata=None):
    return field(default_factory=lambda: default, metadata=metadata)


@dataclass
class BasicExample:
    foo: int
    bar: float
    baz: str
    flag: bool


@dataclass
class WithDefaultExample:
    foo: int = 42
    baz: str = field(default="toto", metadata={"help": "help message"})


@dataclass
class WithDefaultBoolExample:
    foo: bool = False
    baz: bool = True
    opt: Optional[bool] = None


class BasicEnum(Enum):
    titi = "titi"
    toto = "toto"


@dataclass
class EnumExample:
    foo: BasicEnum = "toto"

    def __post_init__(self):
        self.foo = BasicEnum(self.foo)


@dataclass
class OptionalExample:
    foo: Optional[int] = None
    bar: Optional[float] = field(default=None, metadata={"help": "help message"})
    baz: Optional[str] = None
    ces: Optional[List[str]] = list_field(default=[])
    des: Optional[List[int]] = list_field(default=[])


@dataclass
class ListExample:
    foo_int: List[int] = list_field(default=[])
    bar_int: List[int] = list_field(default=[1, 2, 3])
    foo_str: List[str] = list_field(default=["Hallo", "Bonjour", "Hello"])
    foo_float: List[float] = list_field(default=[0.1, 0.2, 0.3])


class SdArgumentParserTest(unittest.TestCase):
    def argparsersEqual(self, a: argparse.ArgumentParser, b: argparse.ArgumentParser) -> bool:
        """
        Small helper to check pseudo-equality of parsed arguments on `ArgumentParser` instances.
        """
        self.assertEqual(len(a._actions), len(b._actions))
        for x, y in zip(a._actions, b._actions):
            xx = {k: v for k, v in vars(x).items() if k != "container"}
            yy = {k: v for k, v in vars(y).items() if k != "container"}
            self.assertEqual(xx, yy)

    def test_basic(self):
        parser = SdArgumentParser(BasicExample)

        expected = argparse.ArgumentParser()
        expected.add_argument("--foo", type=int, required=True)
        expected.add_argument("--bar", type=float, required=True)
        expected.add_argument("--baz", type=str, required=True)
        expected.add_argument("--flag", type=string_to_bool, default=True, const=True, nargs="?")
        self.argparsersEqual(parser, expected)

    def test_with_default(self):
        parser = SdArgumentParser(WithDefaultExample)

        expected = argparse.ArgumentParser()
        expected.add_argument("--foo", default=42, type=int)
        expected.add_argument("--baz", default="toto", type=str, help="help message")
        self.argparsersEqual(parser, expected)

    def test_with_default_bool(self):
        parser = SdArgumentParser(WithDefaultBoolExample)

        expected = argparse.ArgumentParser()
        expected.add_argument("--foo", type=string_to_bool, default=False, const=True, nargs="?")
        expected.add_argument("--no_baz", action="store_false", dest="baz")
        expected.add_argument("--baz", type=string_to_bool, default=True, const=True, nargs="?")
        expected.add_argument("--opt", type=string_to_bool, default=None)
        self.argparsersEqual(parser, expected)

        args = parser.parse_args([])
        self.assertEqual(args, Namespace(foo=False, baz=True, opt=None))

        args = parser.parse_args(["--foo", "--no_baz"])
        self.assertEqual(args, Namespace(foo=True, baz=False, opt=None))

        args = parser.parse_args(["--foo", "--baz"])
        self.assertEqual(args, Namespace(foo=True, baz=True, opt=None))

        args = parser.parse_args(["--foo", "True", "--baz", "True", "--opt", "True"])
        self.assertEqual(args, Namespace(foo=True, baz=True, opt=True))

        args = parser.parse_args(["--foo", "False", "--baz", "False", "--opt", "False"])
        self.assertEqual(args, Namespace(foo=False, baz=False, opt=False))

    def test_with_enum(self):
        parser = SdArgumentParser(EnumExample)

        expected = argparse.ArgumentParser()
        expected.add_argument("--foo", default="toto", choices=["titi", "toto"], type=str)
        self.argparsersEqual(parser, expected)

        args = parser.parse_args([])
        self.assertEqual(args.foo, "toto")
        enum_ex = parser.parse_args_into_dataclasses([])[0]
        self.assertEqual(enum_ex.foo, BasicEnum.toto)

        args = parser.parse_args(["--foo", "titi"])
        self.assertEqual(args.foo, "titi")
        enum_ex = parser.parse_args_into_dataclasses(["--foo", "titi"])[0]
        self.assertEqual(enum_ex.foo, BasicEnum.titi)

    def test_with_list(self):
        parser = SdArgumentParser(ListExample)

        expected = argparse.ArgumentParser()
        expected.add_argument("--foo_int", nargs="+", default=[], type=int)
        expected.add_argument("--bar_int", nargs="+", default=[1, 2, 3], type=int)
        expected.add_argument("--foo_str", nargs="+", default=["Hallo", "Bonjour", "Hello"], type=str)
        expected.add_argument("--foo_float", nargs="+", default=[0.1, 0.2, 0.3], type=float)

        self.argparsersEqual(parser, expected)

        args = parser.parse_args([])
        self.assertEqual(
            args,
            Namespace(foo_int=[], bar_int=[1, 2, 3], foo_str=["Hallo", "Bonjour", "Hello"], foo_float=[0.1, 0.2, 0.3]),
        )

        args = parser.parse_args("--foo_int 1 --bar_int 2 3 --foo_str a b c --foo_float 0.1 0.7".split())
        self.assertEqual(args, Namespace(foo_int=[1], bar_int=[2, 3], foo_str=["a", "b", "c"], foo_float=[0.1, 0.7]))

    def test_with_optional(self):
        parser = SdArgumentParser(OptionalExample)

        expected = argparse.ArgumentParser()
        expected.add_argument("--foo", default=None, type=int)
        expected.add_argument("--bar", default=None, type=float, help="help message")
        expected.add_argument("--baz", default=None, type=str)
        expected.add_argument("--ces", nargs="+", default=[], type=str)
        expected.add_argument("--des", nargs="+", default=[], type=int)
        self.argparsersEqual(parser, expected)

        args = parser.parse_args([])
        self.assertEqual(args, Namespace(foo=None, bar=None, baz=None, ces=[], des=[]))

        args = parser.parse_args("--foo 12 --bar 3.14 --baz 42 --ces a b c --des 1 2 3".split())
        self.assertEqual(args, Namespace(foo=12, bar=3.14, baz="42", ces=["a", "b", "c"], des=[1, 2, 3]))

    def test_parse_dict(self):
        parser = SdArgumentParser(BasicExample)

        args_dict = {
            "foo": 12,
            "bar": 3.14,
            "baz": "42",
            "flag": True,
        }

        parsed_args = parser.parse_dict(args_dict)[0]
        args = BasicExample(**args_dict)
        self.assertEqual(parsed_args, args)
