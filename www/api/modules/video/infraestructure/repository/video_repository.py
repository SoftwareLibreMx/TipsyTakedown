from datetime import datetime
from sqlalchemy.orm import Session

from ...domain.entity import VideoModel, VideoEncodingQueueModel


class VideoRepository:
    def __init__(self, db_engine):
        self.db_engine = db_engine

    def get_video_by_id(self, video_id: str) -> VideoModel:
        with Session(self.db_engine) as session:
            return session.query(VideoModel).filter_by(
                id=video_id, deleted_at=None).first()

    def create_video(self, video: VideoModel) -> VideoModel:
        with Session(self.db_engine) as session:
            session.add(video)
            session.commit()
            session.refresh(video)
            return video

    def update_video(self, video_id: str, video_dict: dict) -> VideoModel:
        with Session(self.db_engine) as session:
            video_db = session.query(VideoModel).filter_by(
                id=video_id, deleted_at=None).first()

            video_db.teacher_id = video_dict.get(
                'teacher_id', video_db.teacher_id)
            video_db.name = video_dict.get('name', video_db.name)
            video_db.description = video_dict.get(
                'description', video_db.description)
            video_db.updated_at = datetime.now()

            session.commit()
            session.refresh(video_db)
            return video_db

    def delete_video(self, video_id: str) -> VideoModel:
        with Session(self.db_engine) as session:
            video_db = session.query(VideoModel).filter_by(
                id=video_id, deleted_at=None).first()

            if not video_db:
                raise Exception('Video not found')

            video_db.soft_delete()
            session.commit()
            session.refresh(video_db)
            return video_db


class VideoEncodingQueuRepository:
    def __init__(self, db_engine):
        '''
        TODO: if needed create independent file, currently is not necessary
        '''
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
