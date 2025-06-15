from http import HTTPStatus

import pytest

from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from fixtures.courses import CourseFixture
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import assert_create_exercise_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.exercises
@pytest.mark.regression
class TestExercises:
    """
    Тестовый класс для проверки функциональности API заданий.
    """

    def test_create_exercise(
        self,
        exercises_client: ExercisesClient,
        function_course: CourseFixture
    ):
        """
        Тест создания задания через POST-запрос к /api/v1/exercises.
        
        Проверяет:
        - Статус-код ответа 200
        - Соответствие тела ответа запросу
        - Валидацию JSON schema ответа
        
        :param exercises_client: Клиент для работы с API заданий
        :param function_course: Фикстура курса для связи с заданием
        """
        # Подготовка данных для запроса
        request = CreateExerciseRequestSchema(
            course_id=function_course.response.course.id
        )
        
        # Выполнение POST-запроса
        response = exercises_client.create_exercise_api(request)
        
        # Проверка статус-кода
        assert_status_code(response.status_code, HTTPStatus.OK)
        
        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)
        
        # Проверяем соответствие JSON-ответа схеме
        validate_json_schema(response.json(), response_data.model_json_schema())
        
        # Проверка соответствия ответа запросу
        assert_create_exercise_response(request, response_data)