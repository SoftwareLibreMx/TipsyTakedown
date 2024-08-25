from typing import Optional

from api.libs.domain_entity import Pagination


class CourseService:
    def __init__(self, course_repository):
        self.course_repository = course_repository

    def get_all(
        self,
        filters: dict,
        pagination: Optional[dict] = {'page': 1, 'per_page': 10}
    ):
        pagination = Pagination(**pagination)

        courses = self.course_repository.get_all(filters, pagination)

        return courses
