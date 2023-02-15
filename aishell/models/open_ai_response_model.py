from typing import List, Optional

from pydantic import BaseModel


class OpenAIResponseModel(BaseModel):

    class Choice(BaseModel):
        finish_reason: str
        index: int
        logprobs: Optional[None]
        text: Optional[str]

    class Usage(BaseModel):
        completion_tokens: int
        prompt_tokens: int
        total_tokens: int

    choices: Optional[List[Choice]]
    created: int
    id: str
    model: str
    object: str
    usage: Usage
