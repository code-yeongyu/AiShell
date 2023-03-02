from enum import Enum
from typing import Any


class StrEnum(str, Enum):

    def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]):  # type: ignore
        return name.lower()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
