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

import dataclasses
import json
import sys
from argparse import ArgumentParser
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, List, NewType, Optional, Tuple, Union

import yaml

DataClass = NewType("DataClass", Any)
DataClassType = NewType("DataClassType", Any)


def string_to_bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise ValueError(
            f"Truthy value expected: got {v} but expected one of yes/no, true/false, t/f, y/n, 1/0 (case insensitive)."
        )


class SdArgumentParser(ArgumentParser):
    """
    ArgumentParser 的子类，主要用于将命令行参数，yaml文件中的参数，json中的参数转换为 dataclass
    """

    dataclass_types: Iterable[DataClassType]

    def __init__(self, dataclass_types: Union[DataClassType, Iterable[DataClassType]], **kwargs):
        """
        Args:
            dataclass_types:
                dataclass的列表
            kwargs:
                (可选) 会传入 `argparse.ArgumentParser()`
        """
        super().__init__(**kwargs)
        if dataclasses.is_dataclass(dataclass_types):
            dataclass_types = [dataclass_types]
        self.dataclass_types = dataclass_types
        for dtype in self.dataclass_types:
            self._add_dataclass_arguments(dtype)

    def _add_dataclass_arguments(self, dtype: DataClassType):
        for field in dataclasses.fields(dtype):
            if not field.init:
                continue
            field_name = f"--{field.name}"
            kwargs = field.metadata.copy()
            # field.metadata is not used at all by Data Classes,
            # it is provided as a third-party extension mechanism.
            if isinstance(field.type, str):
                raise ImportError(
                    "This implementation is not compatible with Postponed Evaluation of Annotations (PEP 563),"
                    "which can be opted in from Python 3.7 with `from __future__ import annotations`."
                    "We will add compatibility when Python 3.9 is released."
                )
            typestring = str(field.type)
            for prim_type in (int, float, str):
                for collection in (List,):
                    if (
                            typestring == f"typing.Union[{collection[prim_type]}, NoneType]"
                            or typestring == f"typing.Optional[{collection[prim_type]}]"
                    ):
                        field.type = collection[prim_type]
                if (
                        typestring == f"typing.Union[{prim_type.__name__}, NoneType]"
                        or typestring == f"typing.Optional[{prim_type.__name__}]"
                ):
                    field.type = prim_type

            if isinstance(field.type, type) and issubclass(field.type, Enum):
                kwargs["choices"] = [x.value for x in field.type]
                kwargs["type"] = type(kwargs["choices"][0])
                if field.default is not dataclasses.MISSING:
                    kwargs["default"] = field.default
            elif field.type is bool or field.type is Optional[bool]:
                if field.default is True:
                    self.add_argument(f"--no_{field.name}", action="store_false", dest=field.name, **kwargs)

                # Hack because type=bool in argparse does not behave as we want.
                kwargs["type"] = string_to_bool
                if field.type is bool or (field.default is not None and field.default is not dataclasses.MISSING):
                    # Default value is True if we have no default when of type bool.
                    default = True if field.default is dataclasses.MISSING else field.default
                    # This is the value that will get picked if we don't include --field_name in any way
                    kwargs["default"] = default
                    # This tells argparse we accept 0 or 1 value after --field_name
                    kwargs["nargs"] = "?"
                    # This is the value that will get picked if we do --field_name (without value)
                    kwargs["const"] = True
            elif hasattr(field.type, "__origin__") and issubclass(field.type.__origin__, List):
                kwargs["nargs"] = "+"
                kwargs["type"] = field.type.__args__[0]
                assert all(
                    x == kwargs["type"] for x in field.type.__args__
                ), "{} cannot be a List of mixed types".format(field.name)
                if field.default_factory is not dataclasses.MISSING:
                    kwargs["default"] = field.default_factory()
            else:
                kwargs["type"] = field.type
                if field.default is not dataclasses.MISSING:
                    kwargs["default"] = field.default
                elif field.default_factory is not dataclasses.MISSING:
                    kwargs["default"] = field.default_factory()
                else:
                    kwargs["required"] = True
            self.add_argument(field_name, **kwargs)

    def parse_args_into_dataclasses(
            self, args=None, return_remaining_strings=False, look_for_args_file=True
    ) -> Tuple[DataClass, ...]:
        """
        将命令行参数转化为指定的dataclass对象。

        主要利用argparse中的ArgumentParser.parse_known_args方法来实现。
        Args:
            args:
                List of strings to parse. The default is taken from sys.argv.
                (same as argparse.ArgumentParser)
            return_remaining_strings:
                If true, also return a list of remaining argument strings.
            look_for_args_file:
                If true, will look for a ".args" file with the same base name
                as the entry point script for this process, and will append its
                potential content to the command line args.

        Returns:
            Tuple consisting of:
                - the dataclass instances in the same order as they
                  were passed to the initializer.abspath
                - if applicable, an additional namespace for more
                  (non-dataclass backed) arguments added to the parser
                  after initialization.
                - The potential list of remaining argument strings.
                  (same as argparse.ArgumentParser.parse_known_args)
        """
        if look_for_args_file and len(sys.argv):
            args_file = Path(sys.argv[0]).with_suffix(".args")
            if args_file.exists():
                fargs = args_file.read_text().split()
                args = fargs + args if args is not None else fargs + sys.argv[1:]
                # in case of duplicate arguments the first one has precedence
                # so we append rather than prepend.
        namespace, remaining_args = self.parse_known_args(args=args)
        outputs = []
        for dtype in self.dataclass_types:
            keys = {f.name for f in dataclasses.fields(dtype)}
            inputs = {k: v for k, v in vars(namespace).items() if k in keys}
            for k in keys:
                delattr(namespace, k)
            obj = dtype(**inputs)
            outputs.append(obj)
        if len(namespace.__dict__) > 0:
            # additional namespace.
            outputs.append(namespace)
        if return_remaining_strings:
            return (*outputs, remaining_args)
        else:
            return (*outputs,)

    def parse_dict(self, args: dict) -> Tuple[DataClass, ...]:
        """
        Alternative helper method that does not use `argparse` at all, instead uses a dict and populating the dataclass
        types.
        """
        outputs = []
        for dtype in self.dataclass_types:
            keys = {f.name for f in dataclasses.fields(dtype) if f.init}
            inputs = {k: v for k, v in args.items() if k in keys}
            obj = dtype(**inputs)
            outputs.append(obj)
        return (*outputs,)

    def parse_json_file(self, json_file: str) -> Tuple[DataClass, ...]:
        """
        从json文件中解析参数
        """
        data = json.loads(Path(json_file).read_text())
        outputs = []
        for dtype in self.dataclass_types:
            keys = {f.name for f in dataclasses.fields(dtype)}
            inputs = {k: v for k, v in data.items() if k in keys}
            obj = dtype(**inputs)
            outputs.append(obj)
        return (*outputs,)

    def parse_json_str(self, json_str: str) -> Tuple[DataClass, ...]:
        """
        从yaml文件中解析参数
        """
        data = json.loads(json_str)
        outputs = []
        for dtype in self.dataclass_types:
            keys = {f.name for f in dataclasses.fields(dtype)}
            inputs = {k: v for k, v in data.items() if k in keys}
            obj = dtype(**inputs)
            outputs.append(obj)
        return (*outputs,)

    def parse_yaml_file(self, yaml_file: str) -> Tuple[DataClass, ...]:
        """
        从yaml文件中解析参数
        """
        with open(yaml_file, encoding='utf-8') as config_data_file:
            data = yaml.safe_load(config_data_file)
        outputs = []
        for dtype in self.dataclass_types:
            keys = {f.name for f in dataclasses.fields(dtype)}
            inputs = {k: v for k, v in data.items() if k in keys}
            obj = dtype(**inputs)
            outputs.append(obj)
        return (*outputs,)
