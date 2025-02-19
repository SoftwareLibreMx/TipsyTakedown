from shared.globals import db_engine

from ...infrastructure.repository import LessonRepository, MaterialRepository
from ...domain.service import LessonService, MaterialService

MATERIAL_REPOSITORY = None
MATERIAL_SERVICE = None
LESSON_REPOSITORY = None
LESSON_SERVICE = None


def __init_classes() -> LessonService:
    global MATERIAL_REPOSITORY, MATERIAL_SERVICE
    global LESSON_SERVICE, LESSON_REPOSITORY

    if not MATERIAL_REPOSITORY:
        MATERIAL_REPOSITORY = MaterialRepository(db_engine)

    if not MATERIAL_SERVICE:
        MATERIAL_SERVICE = MaterialService(MATERIAL_REPOSITORY, None)

    if not LESSON_REPOSITORY:
        LESSON_REPOSITORY = LessonRepository(db_engine)

    if not LESSON_SERVICE:
        LESSON_SERVICE = LessonService(LESSON_REPOSITORY, MATERIAL_SERVICE)

    return LESSON_SERVICE


def search_by_name(query: str):
    lesson_service = __init_classes()

    return lesson_service.search_by_name(query)


def get_detail_by_id(lesson_id: str):
    lesson_service = __init_classes()

    return lesson_service.get_detail_by_id(lesson_id)


def get_by_ids(lesson_ids: list[str]):
    lesson_service = __init_classes()

    return lesson_service.get_by_ids(lesson_ids)
