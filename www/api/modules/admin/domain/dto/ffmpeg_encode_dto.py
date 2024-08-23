from dataclasses import dataclass


@dataclass
class FFMPEGEncodeDTO:
    file_path: str
    file_key: str
    stdout: str
    error: str or None
