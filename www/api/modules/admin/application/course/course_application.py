from threading import Thread

from werkzeug.datastructures import FileStorage

from api.libs.domain_entity import FlaskFile
from shared.globals import db_engine, minion_credentials

from ...infrastructure.repository import CourseRepository, MinioRepository
from ...domain.service import CourseService, MinioService

COURSE_REPOSITORY = None
MINIO_REPOSITORY = None
MINIO_SERVICE = None
COURSE_SERVICE = None


def __init_classes() -> CourseService:
    global COURSE_SERVICE, COURSE_REPOSITORY
    global MINIO_REPOSITORY, MINIO_SERVICE

    if not COURSE_REPOSITORY:
        COURSE_REPOSITORY = CourseRepository(db_engine)

    if not MINIO_REPOSITORY:
        MINIO_REPOSITORY = MinioRepository(
            minion_credentials.get('endpoint'),
            minion_credentials.get('access_key'),
            minion_credentials.get('secret_key'),
            minion_credentials.get('bucket_name'),
            minion_credentials.get('secure')
        )

    if not MINIO_SERVICE:
        MINIO_SERVICE = MinioService(MINIO_REPOSITORY, [])

    if not COURSE_SERVICE:
        COURSE_SERVICE = CourseService(COURSE_REPOSITORY, MINIO_SERVICE)

    return COURSE_SERVICE


def create(user, req_course: dict):
    course_service = __init_classes()

    return course_service.create(user, req_course)


def add_thumbnail_to_course_async(course_id: str, thumbnail_file: FileStorage):
    course_service = __init_classes()

    file_bytes = thumbnail_file.read()

    thumbnail_flask_file = FlaskFile(
        file_name=thumbnail_file.filename,
        mimetype=thumbnail_file.mimetype,
        file_size=len(file_bytes),
        content=file_bytes
    )

    Thread(target=lambda: course_service.add_thumbnail_to_course(
        course_id, thumbnail_flask_file)).start()
