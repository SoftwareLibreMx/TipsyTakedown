from dataclasses import dataclass


@dataclass
class FFMPEGEncodeDTO:
    file_path: str
    stdout: str
