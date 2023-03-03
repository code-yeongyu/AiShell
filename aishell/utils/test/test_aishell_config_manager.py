from aishell.utils import AiShellConfigManager


def test_init_without_path():
    config_manager = AiShellConfigManager()
    assert config_manager.config_path == AiShellConfigManager.DEFAULT_CONFIG_PATH


def test_with_path():
    config_manager = AiShellConfigManager(config_path='test_path')
    assert config_manager.config_path == 'test_path'
