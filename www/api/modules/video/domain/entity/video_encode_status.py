from enum import Enum


class VideoEncodeStatus(Enum):
    PENDING = 'PENDING'
    ENCODING = 'ENCODING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
