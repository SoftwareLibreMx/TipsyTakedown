from api.libs.domain_entity import UserType

from ...entity import CourseModel
from ....infrastructure.repository import CourseRepository


class CourseService:
    __valid_user_types = [UserType.ADMIN.value, UserType.TEACHER.value]

    def __init__(self, course_repo: CourseRepository):
        self.course_repo = course_repo

    def create(self, user, req_course: dict):
        if user.get("user_type") not in self.__valid_user_types:
            return "User is not authorized to create a course", None

        error, course = CourseModel.from_dict({
            "name": req_course.get("name"),
            "description": req_course.get("description"),
            "long_description": req_course.get("long_description"),
            "teacher_id": user.get("id"),
            "lessons": req_course.get("lessons", []),
            "thumbnail": req_course.get("thumbnail"),
            "teaser_material_id": req_course.get("teaser_material_id"),
        })

        if error:
            return error, None

        try:
            course = self.course_repo.create(course)
        except Exception as e:
            return str(e), None

        return None, self.course_repo.create(course)
