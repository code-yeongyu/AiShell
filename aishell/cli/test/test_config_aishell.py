from unittest.mock import MagicMock, patch

from aishell.cli.config_aishell import save_config
from aishell.models import AiShellConfigModel, LanguageModel, RevChatGPTChatbotConfigModel
from aishell.utils import AiShellConfigManager


class TestSaveConfig:

    @patch('aishell.cli.config_aishell.AiShellConfigManager', spec=AiShellConfigManager)
    def test_success_when_config_file_not_available(
        self,
        mocked_config_manager_class: MagicMock,
    ):
        '''config file 이 없는 경우 테스트 성공해야 한다'''
        # given
        mocked_config_manager_class.is_config_file_available.return_value = False

        # when
        save_config('valid_session_token')

        # then
        mocked_config_manager_class.return_value.save_config.assert_called_once()

    @patch('aishell.cli.config_aishell.AiShellConfigManager', spec=AiShellConfigManager)
    def test_success_when_config_file_available_with_chatgpt_config(
        self,
        mocked_config_manager_class: MagicMock,
    ):
        '''config file 이 있고, chatgpt_config 가 있는 경우 테스트 성공해야 한다.'''
        # given
        mocked_config_manager_class.is_config_file_available.return_value = True
        mocked_config_manager_instance = mocked_config_manager_class.return_value
        mocked_config_manager_instance.config_model =\
            AiShellConfigModel(chatgpt_config=RevChatGPTChatbotConfigModel(session_token='invalid_session_token'))

        # when
        save_config('valid_session_token')

        # then
        mocked_config_manager_class.return_value.save_config.assert_called_once()

    @patch('aishell.cli.config_aishell.AiShellConfigManager', spec=AiShellConfigManager)
    def test_success_when_config_file_available_without_chatgpt_config(
        self,
        mocked_config_manager_class: MagicMock,
    ):
        '''config file 이 있고, chatgpt_config 가 없는 경우 테스트 성공해야 한다.'''
        # given
        mocked_config_manager_class.is_config_file_available.return_value = True
        mocked_config_manager_instance = mocked_config_manager_class.return_value
        mocked_config_manager_instance.config_model =\
            AiShellConfigModel(language_model=LanguageModel.GPT3, openai_api_key='valid_openai_api_key')

        # when
        save_config('valid_session_token')

        # then
        mocked_config_manager_class.return_value.save_config.assert_called_once()

    # when config file available - with chatgpt_config
    # when config file available - without chatgpt_config
    # when config file not available
