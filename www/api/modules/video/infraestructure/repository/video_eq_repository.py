from sqlalchemy.orm import Session

from ...domain.entity import VideoEncodingQueueModel, VideoEncodeStatus


class VideoEQRepository:
    def __init__(self, db_engine):
        self.db_engine = db_engine

    def get_first_video_to_encode(self) -> VideoEncodingQueueModel:
        with Session(self.db_engine) as session:
            return session.query(VideoEncodingQueueModel).filter_by(
                status='pending').first()

    def update_status(self, video_id: str,
                      status: VideoEncodeStatus) -> VideoEncodingQueueModel:
        with Session(self.db_engine) as session:
            video_eq = session.query(VideoEncodingQueueModel).filter_by(
                id=video_id).first()

            video_eq.status = status.value
            session.commit()
            session.refresh(video_eq)
            return video_eq
