from enum import Enum


class VideoEncodingQueueStatus(Enum):
    PENDING = 'PENDING'
    ENCODING = 'ENCODING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
