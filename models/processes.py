from enum import Enum


class ProcessStatus(Enum):
    PENDING = "Pending"
    COMPLETE = "Complete"
    FAILURE = "Failure"
