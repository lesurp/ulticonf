# from pathlib import PurePath
# from typing import TYPE_CHECKING, TypeAlias

# if TYPE_CHECKING:
# from _typeshed import SupportsRead
import argparse
from typing import Any, Optional, Type
from logging import debug
import os
import toml

# PathLike: TypeAlias = str | bytes | PurePath

# TODO: abstract over config file types


# TODO add methods for overriding names (split env / key etc.)
class ParameterHandle:
    def __init__(self, dest: str, type: Type) -> None:
        self.dest: str = dest
        self.type: Optional[Type] = type
        self.load_from_env: Optional[bool] = None
        self.load_from_file: Optional[bool] = None

    def from_raw_str(self, value_str: Optional[str]):
        if self.type and value_str:
            debug(f"Converting '{value_str}' to '{self.type}'")
            return self.type(value_str)
        else:
            debug(
                f"Either the type or the value is None - returning the value as-is: '{value_str}'"
            )
            return value_str


class Ulticonf:
    def __init__(
        self,
        environment_prefix: Optional[str] = None,
        configuration_file: Optional[Any] = None,
        *args,
        **kwargs,
    ) -> None:
        # TODO: force environment_prefix if auto_read_env is true?
        self.parser = argparse.ArgumentParser(*args, **kwargs)
        self.environment_prefix = environment_prefix
        if configuration_file is None:
            self._file_loader = None
        else:
            # TODO: handle error
            self._file_loader = toml.load(configuration_file)
        self.parameter_handles = []

    # TODO: add support for arg groups
    # TODO: ignore positional/required arguments (or not, argparse will complain anyway)
    # TODO: add method for looking ONLY at env/file?
    def add_argument(self, *args, **kwargs) -> ParameterHandle:
        action = self.parser.add_argument(*args, **kwargs)
        h = ParameterHandle(action.dest, action.type)
        self.parameter_handles.append(h)
        return h

    def _from_env(self, h: ParameterHandle) -> Optional[Any]:
        debug(f"Loading '{h.dest}' from env")
        if self.environment_prefix is None:
            return None

        env_var_name = self.environment_prefix + h.dest.upper()
        debug(f"Corresponding env. variable name: {env_var_name}")
        value_str = os.environ.get(env_var_name)
        debug(f"Value retrieved: {value_str}")
        return h.from_raw_str(value_str)

    def _from_file(self, h: ParameterHandle) -> Optional[Any]:
        if self._file_loader is None:
            return None
        value_str = self._file_loader.get(h.dest)
        return h.from_raw_str(value_str)

    def parse_args(self, args=None, namespace=None):
        debug("parse_args called, first getting value from argparse")
        from_cli = self.parser.parse_args(args, namespace)
        debug(f"Got: {from_cli}")
        for h in self.parameter_handles:
            debug(f"Processing parameter with dest = {h.dest}")
            value = getattr(from_cli, h.dest)
            if value is not None:
                debug(f"Was defined in cli args, value = {value}")
                continue
            value = self._from_env(h)
            if value is not None:
                debug(f"Was defined in env variables, value = {value}")
                setattr(from_cli, h.dest, value)
                continue
            value = self._from_file(h)
            if value is not None:
                debug(f"Was defined in configuration file, value = {value}")
                setattr(from_cli, h.dest, value)
                continue
            debug(f"Was NOT defined, value is None")
        return from_cli
