from typing import Optional

from api.libs.utils import as_dict

from api.modules.admin.infrastructure.repository import LessonRepository
from api.modules.admin.domain.entity import LessonModel


class LessonService:
    def __init__(self, lesson_repository: LessonRepository):
        self.lesson_repository = lesson_repository

    def update_or_create(
        self,
        lessons: dict | list[dict]
    ) -> tuple[Optional[str], Optional[str]]:
        if isinstance(lessons, dict):
            lessons = [lessons]

        missing_lessons = []
        for index, lesson in enumerate(lessons):
            if lesson.get("id"):
                self.lesson_repository.update(lesson)
                continue

            lessons[index] = None
            missing_lessons.append(LessonModel.from_dict(lesson))

        try:
            missing_lessons = self.lesson_repository.create_all(
                missing_lessons
            )
        except Exception as e:
            print('Cannot create', e)
            return str(e), None

        lesson_ids = []
        for index, lesson in enumerate(lessons):
            if lesson:
                lesson_ids.append(lesson.get("id"))
                continue

            lessons = missing_lessons.pop(0)
            lesson_ids.append(lessons.id)

        return None, lesson_ids

    def search_by_name(self, query: str):
        lessons_db = self.lesson_repository.search_by_name(query)

        lessons = []
        for lesson in lessons_db:
            lessons.append({
                'name': lesson.name,
                'id': lesson.id
            })

        return lessons

    def get_by_ids(self, lesson_ids: list[str]):
        lessons_db = self.lesson_repository.get_by_ids(lesson_ids)

        lesson_map = {}

        for lesson in lessons_db:
            lesson_map[lesson.id] = as_dict(lesson)

        return [lesson_map.get(lesson_id) for lesson_id in lesson_ids]
