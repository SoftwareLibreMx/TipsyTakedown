from sqlalchemy.orm import Session

from api.modules.admin.domain.entity import (
    VideoEncodingQueueModel, VideoEncodingQueueStatus
)


class VideoEQRepository:
    def __init__(self, db_engine):
        self.db_engine = db_engine

    def create_encoding_queue(self, video_id: str,
                              file_key: str) -> VideoEncodingQueueModel:
        with Session(self.db_engine) as session:
            video_encoding_queue = VideoEncodingQueueModel(
                video_id=video_id, file_key=file_key
            )

            session.add(video_encoding_queue)
            session.commit()
            session.refresh(video_encoding_queue)
            return video_encoding_queue

    def get_first_video_to_encode(self) -> VideoEncodingQueueModel:
        with Session(self.db_engine) as session:
            return session.query(VideoEncodingQueueModel).filter_by(
                status=VideoEncodingQueueStatus.PENDING.value
            ).first()

    def update_status(
        self,
        video_id: str,
        status: VideoEncodingQueueStatus
    ) -> VideoEncodingQueueModel:
        with Session(self.db_engine) as session:
            video_eq = session.query(VideoEncodingQueueModel).filter_by(
                id=video_id).first()

            video_eq.status = status.value
            session.commit()
            session.refresh(video_eq)
            return video_eq
