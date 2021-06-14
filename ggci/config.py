import os
import logging
from typing import Any, Dict, Optional

import yaml

_LOGGER = logging.getLogger(__name__)


class ConfigError(Exception):
    pass


class Config:
    def __init__(
        self,
        ggci_secret: str,
        user_mappings: Optional[Dict[int, int]] = None,
        **kwargs,
    ):
        """GGCI configuration.

        Can be loaded to the GGCI Flask app by using
        `app.config.from_object(dict(Config(...)))`.
        """
        if user_mappings is None:
            user_mappings = {}

        if not isinstance(ggci_secret, str):
            raise TypeError(
                f'ggci-secret must be of type str, got: {type(ggci_secret)}'
            )
        if not isinstance(user_mappings, dict):
            raise TypeError(
                f'user_mappings must be of type dict, got:'
                f' {type(user_mappings)}'
            )

        self._config_dict = {
            'GGCI_SECRET': ggci_secret,
            'GGCI_USER_MAPPINGS': user_mappings,
            **{key.upper(): val for key, val in kwargs.items()},
        }

    def __getitem__(self, key: str) -> Any:
        return self._config_dict[key.upper()]

    def __iter__(self):
        for key, val in self._config_dict.items():
            yield key, val

    def __len__(self):
        return len(self._config_dict)


def load_yaml_config(file_path: Optional[str] = None) -> Config:
    """Loads GGCI configuration from YAML file.

    :param file_path: Path to the YAML config file. If not specified,
     file path from environment variable GGCI_CONFIG is used.
    :type file_path: Optional[str], optional
    :return: GGCI configuration object
    :rtype: Config
    """

    if file_path is None:
        _LOGGER.info(
            'Config file path not specified, using env variable GGCI_CONFIG...'
        )
        try:
            file_path = os.environ['GGCI_CONFIG']
        except KeyError as exc:
            raise ConfigError(
                'Neither file_path argument was supplied nor GGCI_CONFIG'
                ' environment variable was found.'
                ' Cannot load configuration.'
            ) from exc

    _LOGGER.info('Loading GGCI config from file %s...', file_path)

    with open(file_path) as cfg_file:
        try:
            cfg_dict = yaml.safe_load(cfg_file)
        except yaml.YAMLError as exc:
            raise ConfigError('Error loading config file') from exc

    return Config(**cfg_dict)
