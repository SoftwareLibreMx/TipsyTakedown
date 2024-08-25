from shared.globals import db_engine

from ...infrastructure.repository import CourseRepository
from ...domain.service import CourseService

COURSE_REPOSITORY = CourseRepository(db_engine)
COURSE_SERVICE = CourseService(COURSE_REPOSITORY)


def __init_classes() -> CourseService:
    global COURSE_SERVICE, COURSE_REPOSITORY

    if not COURSE_REPOSITORY:
        COURSE_REPOSITORY = CourseRepository(db_engine)

    if not COURSE_SERVICE:
        COURSE_SERVICE = CourseService(COURSE_REPOSITORY)

    return COURSE_SERVICE


def create(user, req_course: dict):
    course_service = __init_classes()

    return course_service.create(user, req_course)
