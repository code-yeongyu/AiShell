import json
import os
from typing import Optional

from aishell.models import AiShellConfigModel


class AiShellConfigManager:
    DEFAULT_CONFIG_PATH = os.path.expanduser('~/.aishell_config.json')

    def __init__(
        self,
        config_model: Optional[AiShellConfigModel] = None,
        config_path: Optional[str] = None,
        load_config: bool = False,
    ):
        '''
        Initialize an instance of AiShellConfigManager

        Args:
            config_model: \
                    An instance of AiShellConfigManager to use as the configuration.\
                    If None and load_config is True, loads the configuration from the configuration file.
            config_path: Path to the configuration file. \
                If None, uses the default path "~/.aishell_config.json".
            load_config: If True and config_model is None, loads the configuration from the configuration file.
        '''
        self.config_path = config_path or AiShellConfigManager.DEFAULT_CONFIG_PATH

        if config_model:
            self.update_config(config_model)
        elif load_config:
            self.load_config()

    @staticmethod
    def is_config_file_available(config_path: str) -> bool:
        return os.path.isfile(config_path)

    def update_config(self, config_model: AiShellConfigModel):
        self.config_model = config_model

    def load_config(self):
        self.config_model = AiShellConfigModel.parse_file(self.config_path)

    def save_config(self):
        with open(self.config_path, 'w') as aishell_config_path:
            config_dict = self.config_model.dict()
            aishell_config_path.write(json.dumps(config_dict, indent=4, sort_keys=True))
