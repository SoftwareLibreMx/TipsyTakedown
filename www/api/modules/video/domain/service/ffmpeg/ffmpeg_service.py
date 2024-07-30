from api.modules.video.domain.dto import FFMPEGEncodeDTO
from api.modules.video.infraestructure.repository import FFMPEGRepository


class FFMPEGService:
    local_prefix = './tmp'

    def __init__(self, ffmpeg_repository: FFMPEGRepository):
        self.ffmpeg_repository = ffmpeg_repository

    def encode(self, scale: str, file_name: str) -> FFMPEGEncodeDTO:
        output_f_name = f'{file_name}_output_{scale}.mp4'
        file_output_path = f'{self.local_prefix}/{output_f_name}'
        file_path = f'{self.local_prefix}/{file_name}'

        print(f'FFMPEGService: Start encoding {file_name} to {scale}')
        resp = self.ffmpeg_repository.encode(
            scale, file_path, file_output_path
        )
        print(f'FFMPEGService: Finish encoding {file_name} to {scale}')

        error = None
        lower_resp = resp.lower().split('error', 1)
        if len(lower_resp) > 1:
            error = lower_resp[1].strip()

        not_found = resp.lower().find('no such file or directory')
        if not_found != -1:
            error = 'No such file or directory'

        return FFMPEGEncodeDTO(
            file_path=file_output_path,
            file_key=output_f_name,
            stdout=resp,
            error=error
        )
