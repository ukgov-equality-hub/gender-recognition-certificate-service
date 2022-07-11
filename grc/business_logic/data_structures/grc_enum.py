from enum import Enum


class GrcEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name
