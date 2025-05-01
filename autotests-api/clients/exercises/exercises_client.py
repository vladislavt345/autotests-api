from clients.api_client import APIClient
from httpx import Response


class ExercisesClient(APIClient):
    """
    Клиент для взаимодействия с эндпоинтами /api/v1/exercises.
    """

    def get_exercises_api(self, courseid: int) -> Response:
        """
        Получение списка заданий для определенного курса.

        :param courseid: ID курса.
        :return: Ответ сервера с данными заданий (httpx.Response).
        """
        params = {"course": courseid}
        return self.get("/api/v1/exercises", params=params)

    def get_exercise_api(self, courseId: int) -> Response:
        """
        Получение информации о задании по его ID.

        :param courseId: ID задания.
        :return: Ответ сервера с данными о задании (httpx.Response).
        """
        return self.get(f"/api/v1/exercises/{courseId}")

    def create_exercise_api(self, payload: dict) -> Response:
        """
        Создание нового задания.

        :param payload: Словарь с данными: title, courseId, maxScore, minScore, orderIndex, description, estimatedTime.
        :return: Ответ от сервера (httpx.Response).
        """
        return self.post("/api/v1/exercises", json=payload)

    def update_exercise_api(self, courseId: int, payload: dict) -> Response:
        """
        Частичное обновление задания по ID.

        :param courseId: ID задания.
        :param payload: Словарь с обновляемыми полями: title, maxScore, minScore, orderIndex, description, estimatedTime.
        :return: Ответ от сервера (httpx.Response).
        """
        return self.patch(f"/api/v1/exercises/{courseId}", json=payload)

    def delete_exercise_api(self, courseId: int) -> Response:
        """
        Удаление задания.

        :param courseId: ID задания.
        :return: Ответ сервера после удаления (httpx.Response).
        """
        return self.delete(f"/api/v1/exercises/{courseId}")