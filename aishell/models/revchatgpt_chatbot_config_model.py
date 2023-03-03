from typing import Optional

from pydantic import BaseModel, root_validator


class RevChatGPTChatbotConfigModel(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    session_token: Optional[str] = None
    access_token: Optional[str] = None
    paid: bool = False

    @root_validator
    def check_at_least_one_account_info(cls, values: dict[str, Optional[str]]):
        IS_ACCOUNT_LOGIN = values.get('email') and values.get('password')
        IS_TOKEN_AUTH = values.get('session_token') or values.get('access_token')
        if not IS_ACCOUNT_LOGIN and not IS_TOKEN_AUTH:
            raise ValueError('No information for authentication provided.')

        return values

    class Config:
        frozen = True
