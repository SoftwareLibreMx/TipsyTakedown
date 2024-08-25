from shared.globals import db_engine

from ...domian.service import CourseService
from ...infrastructure.repository import CourseRepository

COURSE_REPOSITORY = None
COURSE_SERVICE = None


def __init_classes() -> CourseService:
    global COURSE_REPOSITORY, COURSE_SERVICE

    if not COURSE_REPOSITORY:
        COURSE_REPOSITORY = CourseRepository(db_engine)

    if not COURSE_SERVICE:
        COURSE_SERVICE = CourseService(COURSE_REPOSITORY)

    return COURSE_SERVICE


def get_all(filters: dict, pagination: dict):
    course_service = __init_classes()

    courses_model = course_service.get_all(filters, pagination)

    json_resp = []
    for course in courses_model:
        json_resp.append(course.__dict__)

    return None, json_resp
