from shared.globals import db_engine

from ...infrastructure.repository import LessonRepository
from ...domain.service import LessonService

LESSON_REPOSITORY = None
LESSON_SERVICE = None


def __init_classes() -> LessonService:
    global LESSON_SERVICE, LESSON_REPOSITORY

    if not LESSON_REPOSITORY:
        LESSON_REPOSITORY = LessonRepository(db_engine)

    if not LESSON_SERVICE:
        LESSON_SERVICE = LessonService(LESSON_REPOSITORY)

    return LESSON_SERVICE


def search_by_name(query: str):
    lesson_service = __init_classes()

    return lesson_service.search_by_name(query)
