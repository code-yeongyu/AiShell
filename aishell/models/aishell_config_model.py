from typing import Optional

from pydantic import BaseModel, root_validator

from .language_model import LanguageModel
from .revchatgpt_chatbot_config_model import RevChatGPTChatbotConfigModel


class AiShellConfigModel(BaseModel):
    language_model: LanguageModel = LanguageModel.REVERSE_ENGINEERED_CHATGPT
    chatgpt_config: Optional[RevChatGPTChatbotConfigModel] = None
    openai_api_key: Optional[str] = None

    @root_validator
    def check_required_info_provided(cls, values: dict[str, Optional[str]]):
        OPENAI_API_KEY_REQUIRED_MODELS = (LanguageModel.GPT3, LanguageModel.OFFICIAL_CHATGPT)

        language_model = values.get('language_model')
        if language_model in OPENAI_API_KEY_REQUIRED_MODELS:
            if not values.get('openai_api_key'):
                raise ValueError('openai_api_key should not be none')
        elif language_model == LanguageModel.REVERSE_ENGINEERED_CHATGPT:
            if not values.get('chatgpt_config'):
                raise ValueError('chatgpt_config should not be none')

        return values
