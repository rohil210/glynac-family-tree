from __future__ import annotations

from enum import Enum


class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"

    @classmethod
    def from_string(cls, value: str) -> Gender | None:
        normalized = value.strip().lower()
        for gender in cls:
            if gender.value.lower() == normalized:
                return gender
        return None
