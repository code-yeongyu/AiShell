from enum import Enum
from typing import Any


class StrEnum(str, Enum):

    def _generate_next_value_(  # pyright: ignore [reportIncompatibleMethodOverride], for pyright's bug
        name: str,
        start: int,
        count: int,
        last_values: list[Any],
    ):
        return name.lower()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
