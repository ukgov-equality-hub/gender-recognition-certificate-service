import enum


class ListStatus(enum.Enum):
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN PROGRESS"
    NOT_STARTED = "NOT STARTED"
    CANNOT_START_YET = "CANNOT START YET"
    IN_REVIEW = "IN REVIEW"  # Value 'in progress' is used only at task list
    ERROR = "ERROR"
