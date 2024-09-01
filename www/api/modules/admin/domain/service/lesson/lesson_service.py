from api.modules.admin.infrastructure.repository import LessonRepository


class LessonService:
    def __init__(self, lesson_repository: LessonRepository):
        self.lesson_repository = lesson_repository

    def search_by_name(self, query: str):
        lessons_db = self.lesson_repository.search_by_name(query)

        lessons = []
        for lesson in lessons_db:
            lessons.append(lesson[0])

        return lessons

    def get_by_ids(self, lesson_ids: list[str]):
        lessons_db = self.lesson_repository.get_by_ids(lesson_ids)

        return lessons_db
