from api.libs.domain_entity import UserType
from api.libs.domain.entity import CourseModel

from api.modules.admin.infrastructure.repository import CourseRepository
from api.modules.admin.domain.service.minio.minio_service import MinioService


class CourseService:
    __valid_user_types = [UserType.ADMIN.value, UserType.TEACHER.value]

    def __init__(self, course_repo: CourseRepository,
                 minio_service: MinioService):
        self.course_repo = course_repo
        self.minio_service = minio_service

    def create(self, user, req_course: dict):
        if user.get("user_type") not in self.__valid_user_types:
            return "User is not authorized to create a course", None

        error, course = CourseModel.from_dict({
            "name": req_course.get("name"),
            "description": req_course.get("description"),
            "long_description": req_course.get("long_description"),
            "thumbnail": req_course.get("thumbnail", None),
            "teacher_id": user.get("id"),
            "lessons": req_course.get("lessons", []),
            "teaser_material_id": req_course.get("teaser_material_id"),
        })

        if error:
            return error, None

        try:
            course = self.course_repo.create(course)
        except Exception as e:
            return str(e), None

        return None, self.course_repo.create(course)

    def add_thumbnail_to_course(self, course_id: str, thumbnail_file):
        course = self.course_repo.get_by_id(course_id)
        if not course:
            return "Course not found"

        file_extension = thumbnail_file.file_name.split('.')[-1]
        file_key = f'course/{course_id}/thumbnail.{file_extension}'

        self.minio_service.upload_flask_file(file_key, thumbnail_file)

        self.course_repo.update(course_id, {
            "thumbnail": file_key
        })

        return None
