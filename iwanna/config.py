import os
from pathlib import Path
from typing import Any, Dict, KeysView, Optional

import tomli


class Config:
    def __init__(self, data: Dict, is_root: bool = False) -> None:
        self.is_root = is_root
        self.__data = data

    def __str__(self) -> str:
        return str(self._data)

    def __repr__(self) -> str:
        return str(self._data)

    def __getitem__(self, item: str) -> Any:
        if "." in item:
            item, attr = item.split(".", 1)
            value = self._data.get(item, {})
            return Config(value).__getitem__(attr)
        value = self._data.get(item, {})
        if isinstance(value, dict):
            return Config(value)
        return value

    def __setitem__(self, item: str, value: Any) -> None:
        if "." in item:
            item, attr = item.split(".", 1)
            subitem = self._data.get(item, {})
            Config(subitem).__setitem__(attr, value)
            return

        self.__data[item] = value

    def __getattr__(self, item: str) -> Any:
        return self.__getitem__(item)

    def __bool__(self) -> bool:
        if self._data:
            return True
        else:
            return False

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Any:
        return self._data.__iter__()

    def __contains__(self, item: Any) -> Any:
        return self._data.__contains__(item)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Config):
            return bool(self._data == other._data)
        elif isinstance(other, dict):
            return bool(self._data == other)
        else:
            return False

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def keys(self) -> KeysView:
        return self._data.keys()

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self._data.get(key, default)

    @property
    def _data(self) -> Dict:
        self.__lazy_env_set()
        return self.__data

    def __lazy_env_set(self) -> None:
        if self.__data or not self.is_root:
            return
        self.load_toml_file()

    def load_toml_file(self) -> None:
        raw_toml_data = ""

        try:
            for config_path in (
                os.path.join(Path.home(), ".config", "iwanna", "config.toml"),
                os.path.join(Path.home(), ".iwanna", "config.toml"),
            ):
                if os.path.exists(config_path):
                    raw_toml_data = open(config_path, "rb").read().decode()
                    if raw_toml_data and raw_toml_data.strip():
                        break

            if raw_toml_data and raw_toml_data.strip():
                config_dict: Dict = tomli.loads(raw_toml_data)
                self.__data = config_dict
        except tomli.TOMLDecodeError:
            pass


config: Config = Config({}, is_root=True)
