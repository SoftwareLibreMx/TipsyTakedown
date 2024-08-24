from api.libs.domain_entity import Pagination


class CourseService:
    def __init__(self, course_repository):
        self.course_repository = course_repository

    def get_all(
        self,
        filters: dict,
        pagination=Pagination(page=1, per_page=20)
    ):
        return self.course_repository.get_all(filters, pagination)
