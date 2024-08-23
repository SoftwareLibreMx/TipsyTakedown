import os

from shared.globals import local_prefix

from api.modules.admin.domain.dto import FFMPEGEncodeDTO
from api.modules.admin.infrastructure.repository import FFMPEGRepository


class FFMPEGService:
    def __init__(self, ffmpeg_repository: FFMPEGRepository):
        self.ffmpeg_repository = ffmpeg_repository

    def encode(self, scale: str, file_key: str,
               output_file_key: str) -> FFMPEGEncodeDTO:
        output_file_path = f'{local_prefix}/{output_file_key}'
        file_path = f'{local_prefix}/{file_key}'

        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        print(f'FFMPEGService: Start encoding {file_key} to {scale}')
        resp = self.ffmpeg_repository.encode(
            scale, file_path, output_file_path
        )
        print(f'FFMPEGService: Finish encoding {file_key} to {scale}')

        error = None
        lower_resp = resp.lower().split('error', 1)
        if len(lower_resp) > 1:
            error = lower_resp[1].strip()

        not_found = resp.lower().find('no such file or directory')
        if not_found != -1:
            error = resp

        return FFMPEGEncodeDTO(
            file_path=output_file_path,
            file_key=output_file_key,
            stdout=resp,
            error=error
        )
