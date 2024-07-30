from dataclasses import dataclass

from ...entity.video_model import VideoModel


@dataclass
class VideoResponseDTO():
    id: str
    teacher_id: str
    name: str
    description: str
    urls: list[str]

    @staticmethod
    def from_entity(video: VideoModel):
        return VideoResponseDTO(
            id=video.id,
            teacher_id=video.teacher_id,
            name=video.name,
            description=video.description)
