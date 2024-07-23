from dataclasses import dataclass

MIME_TYPE_TO_FILE_EXTENSION = {
    "video/mp4": "mp4",
    "video/webm": "webm",
    "video/ogg": "ogg",
    "video/quicktime": "mov",
    "video/quicktime; codecs=hevc": "hevc",
    "video/x-msvideo": "avi",
    "video/x-flv": "flv",
    "video/x-ms-wmv": "wmv",
    "video/x-matroska": "mkv",
    "video/3gpp": "3gp",
    "video/x-ms-asf": "asf",
    "video/x-m4v": "m4v",
    "video/x-ms-vob": "vob",
}


@dataclass
class FlaskFile:
    file_name: str
    mimetype: str
    file_size: int
    content: bytes

    def get_file_extension(self):
        return MIME_TYPE_TO_FILE_EXTENSION.get(self.mimetype, '')
