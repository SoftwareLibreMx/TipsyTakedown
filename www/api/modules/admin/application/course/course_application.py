from threading import Thread

from werkzeug.datastructures import FileStorage

from api.libs.domain_entity import FlaskFile
from shared.globals import db_engine, minion_credentials

from ...infrastructure.repository import (
    CourseRepository, MinioRepository,
    LessonRepository, MaterialRepository
)
from ...domain.service import (
    CourseService, MinioService,
    LessonService, MaterialService
)

MINIO_REPOSITORY = None
MINIO_SERVICE = None

LESSON_REPOSITORY = None
LESSON_SERVICE = None

MATERIAL_REPOSITORY = None
MATERIAL_SERVICE = None

COURSE_REPOSITORY = None
COURSE_SERVICE = None


def __init_classes() -> CourseService:
    global MINIO_REPOSITORY, MINIO_SERVICE
    global LESSON_REPOSITORY, LESSON_SERVICE
    global MATERIAL_REPOSITORY, MATERIAL_SERVICE
    global COURSE_SERVICE, COURSE_REPOSITORY

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

    if not LESSON_REPOSITORY:
        LESSON_REPOSITORY = LessonRepository(db_engine)

    if not LESSON_SERVICE:
        LESSON_SERVICE = LessonService(LESSON_REPOSITORY)

    if not MATERIAL_REPOSITORY:
        MATERIAL_REPOSITORY = MaterialRepository(db_engine)

    if not MATERIAL_SERVICE:
        MATERIAL_SERVICE = MaterialService(MATERIAL_REPOSITORY, MINIO_SERVICE)

    if not COURSE_REPOSITORY:
        COURSE_REPOSITORY = CourseRepository(db_engine)

    if not COURSE_SERVICE:
        COURSE_SERVICE = CourseService(
            COURSE_REPOSITORY, LESSON_SERVICE,
            MATERIAL_SERVICE, MINIO_SERVICE
        )

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


def get_detail(user, course_id):
    course_service = __init_classes()

    return course_service.get_detail(user, course_id)
