from ...entity import CourseModel
from ....infrastructure.repository import CourseRepository


class CourseService:
    def __init__(self, course_repo: CourseRepository):
        self.course_repo = course_repo

    def create(self, req_course: dict):
        error, course = CourseModel.from_dict(req_course)

        if error:
            return error, None

        try:
            course = self.course_repo.create(course)
        except Exception as e:
            return str(e), None

        return None, self.course_repo.create(course)
