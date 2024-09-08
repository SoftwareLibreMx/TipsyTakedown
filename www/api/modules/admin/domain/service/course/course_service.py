from api.libs.domain_entity import UserType
from api.libs.domain.entity import CourseModel
from api.libs.utils import as_dict

from api.modules.admin.infrastructure.repository import CourseRepository
from api.modules.admin.domain.service.minio.minio_service import MinioService
from ..lesson import LessonService
from ..material import MaterialService


class CourseService:
    __valid_user_types = [UserType.ADMIN.value, UserType.TEACHER.value]

    def __init__(self, course_repo: CourseRepository,
                 lesson_service: LessonService,
                 material_service: MaterialService,
                 minio_service: MinioService):
        self.course_repo = course_repo
        self.lesson_service = lesson_service
        self.material_service = material_service
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

    def update(self, user, course_id, req_course):
        if user.get("user_type") not in self.__valid_user_types:
            return "User is not authorized to update a course", None

        course = self.course_repo.get_by_id(course_id)
        if not course:
            return "Course not found", None

        if req_course.get("lessons"):
            error, lesson_ids = self.lesson_service.update_or_create(
                req_course.get("lessons")
            )

            if error:
                return error, None

            req_course["lessons"] = lesson_ids

        return None, as_dict(self.course_repo.update(course_id, req_course))

    def get_detail(self, user, course_id):
        if user.get("user_type") not in self.__valid_user_types:
            return "User is not authorized to get course detail", None

        try:
            course = self.course_repo.get_by_id(course_id)
        except Exception as e:
            print(e)
            return ["Error while getting course detail"], None

        if not course:
            return "Course not found", None

        course.lessons = self.lesson_service.get_by_ids(course.lessons)

        materials = []
        for lesson in course.lessons:
            materials.extend(lesson.get('materials', []))

        materials = self.material_service.get_by_ids(materials)

        for lesson in course.lessons:
            lesson['materials'] = [
                materials[material_id] for material_id in lesson['materials']
            ]

        return None, as_dict(course)
