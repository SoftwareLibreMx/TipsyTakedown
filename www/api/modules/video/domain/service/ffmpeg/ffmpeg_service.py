from api.modules.video.domain.dto import FFMPEGEncodeDTO
from api.modules.video.infraestructure.repository import FFMPEGRepository


class FFMPEGService:
    local_prefix = './tmp'

    def __init__(self, ffmpeg_repository: FFMPEGRepository):
        self.ffmpeg_repository = ffmpeg_repository

    def encode(self, scale: str, file_name: str) -> FFMPEGEncodeDTO:
        output_f_name = f'{file_name}_output_{scale}.mp4'
        file_output_path = f'{self.local_prefix}/{output_f_name}'

        resp = self.ffmpeg_repository.encode(
            scale=scale,
            file_name=file_name,
            file_output_path=file_output_path
        )

        error = None
        lower_resp = resp.lower().split('error', 1)
        if len(lower_resp) > 1:
            error = lower_resp[1].strip()

        return FFMPEGEncodeDTO(
            file_path=file_output_path,
            stdout=resp,
            error=error
        )
