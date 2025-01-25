import json
import os
import yaml

from abc import ABC, abstractmethod


class ConfigLoader(ABC):
    @abstractmethod
    def load(self, config_path: str) -> dict:
        pass


class JsonConfigLoader(ConfigLoader):
    def load(self, config_path: str) -> dict:
        if not os.path.isfile(config_path):
            raise FileNotFoundError(f"Конфигурационный файл '{config_path}' не найден.")
        with open(config_path, "r") as f:
            return json.load(f)


class YamlConfigLoader(ConfigLoader):
    def load(self, config_path: str) -> dict:
        if not os.path.isfile(config_path):
            raise FileNotFoundError(f"Конфигурационный файл '{config_path}' не найден.")
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
