from enum import auto

from .str_enum import StrEnum


class LanguageModel(StrEnum):
    OFFICIAL_CHATGPT = auto()
    REVERSE_ENGINEERED_CHATGPT = auto()
    GPT3 = auto()
