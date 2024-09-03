
from dataclasses import dataclass

from api.libs.domain.entity import MaterialModel


@dataclass
class MaterialResponseDTO():
    id: str
    teacher_id: str
    name: str
    description: str
    urls: list[str]

    @staticmethod
    def from_entity(video: MaterialModel):
        return MaterialResponseDTO(
            id=video.id,
            teacher_id=video.teacher_id,
            name=video.name,
            description=video.description,
            urls=None)
