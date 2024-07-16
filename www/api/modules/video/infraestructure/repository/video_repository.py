from sqlalchemy.orm import Session

from ...domain.entity import VideoModel


class VideoRepository:
    def __init__(self, db_engine):
        self.db_engine = db_engine

    def get_video_by_id(self, video_id: str) -> VideoModel:
        with Session(self.db_engine) as session:
            return session.query(VideoModel).filter_by(id=video_id).first()

    def create_video(self, video: VideoModel) -> VideoModel:
        with Session(self.db_engine) as session:
            session.add(video)
            session.commit()
            session.refresh(video)
            return video
