from http import HTTPStatus

import pytest

from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    GetExerciseResponseSchema,
    GetExercisesQuerySchema,
    GetExercisesResponseSchema,
    UpdateExerciseRequestSchema
)

from clients.errors_schema import InternalErrorResponseSchema
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.assertions.base import assert_status_code

from tools.assertions.exercises import (
    assert_create_exercise_response,
    assert_get_exercise_response,
    assert_get_exercises_response,
    assert_update_exercise_response,
    assert_exercise_not_found_response
)

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

    def test_get_exercises(
        self,
        exercises_client: ExercisesClient,
        function_exercise: ExerciseFixture,
        function_course: CourseFixture
    ):
        """
        Тест получения списка заданий через GET-запрос к /api/v1/exercises.

        Проверяет:
        - Статус-код ответа 200
        - Соответствие тела ответа списку созданных заданий
        - Валидацию JSON schema ответа

        :param exercises_client: Клиент для работы с API заданий
        :param function_exercise: Фикстура созданного задания
        :param function_course: Фикстура курса для фильтрации заданий
        """
        # Подготовка параметров запроса для фильтрации по курсу
        query = GetExercisesQuerySchema(course_id=function_course.response.course.id)

        # Выполнение GET-запроса для получения списка заданий
        response = exercises_client.get_exercises_api(query)

        # Проверка статус-кода ответа
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = GetExercisesResponseSchema.model_validate_json(response.text)

        # Проверяем соответствие JSON-ответа схеме
        validate_json_schema(response.json(), response_data.model_json_schema())

        # Проверяем, что список заданий содержит созданное задание
        assert_get_exercises_response(response_data, function_exercise.response)

#GET
    def test_get_exercise(
        self,
        exercises_client: ExercisesClient,
        function_exercise: ExerciseFixture
    ):
        """
        Тест получения задания через GET-запрос к /api/v1/exercises/{exercise_id}.

        Проверяет:
        - Успешное получение задания по ID
        - Соответствие статус-кода 200
        - Соответствие данных ответа созданному заданию
        - Валидацию JSON schema ответа

        :param exercises_client: Клиент для работы с API заданий
        :param function_exercise: Фикстура созданного задания
        """
        # Получаем ID задания из фикстуры
        exercise_id = function_exercise.response.exercise.id

        # Выполняем GET-запрос для получения задания
        response = exercises_client.get_exercise_api(exercise_id)

        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        # Проверяем соответствие JSON-ответа схеме
        validate_json_schema(response.json(), response_data.model_json_schema())

        # Проверяем, что полученное задание соответствует созданному
        assert_get_exercise_response(response_data, function_exercise.response)

#PATCH
    def test_update_exercise(
        self,
        exercises_client: ExercisesClient,
        function_exercise: ExerciseFixture
    ):
        """
        Тест обновления задания через PATCH-запрос к /api/v1/exercises/{exercise_id}.

        Проверяет:
        - Успешное обновление задания по ID
        - Соответствие статус-кода 200
        - Соответствие данных ответа запросу на обновление
        - Валидацию JSON schema ответа

        :param exercises_client: Клиент для работы с API заданий
        :param function_exercise: Фикстура созданного задания для обновления
        """
        # Получаем ID задания из фикстуры
        exercise_id = function_exercise.response.exercise.id

        # Подготовка данных для обновления задания
        update_request = UpdateExerciseRequestSchema()

        # Выполняем PATCH-запрос для обновления задания
        response = exercises_client.update_exercise_api(exercise_id, update_request)

        # Проверяем статус-кода ответа
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Десериализуем JSON-ответа в Pydantic-модель
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        # Проверяем соответствие JSON-ответа схеме
        validate_json_schema(response.json(), response_data.model_json_schema())

        # Проверяем, что обновленное задание соответствует запросу
        assert_update_exercise_response(update_request, response_data)


#DELETE
    def test_delete_exercise(
        self,
        exercises_client: ExercisesClient,
        function_exercise: ExerciseFixture
    ):
        """
        Тест удаления задания через DELETE-запрос к /api/v1/exercises/{exercise_id}.

        Проверяет:
        - Статус-код 200 после удаления.
        - Статус-код 404 и соответствующее сообщение об ошибке после попытки получения удаленного задания.
        - Валидацию JSON schema ответа на GET-запрос после удаления.

        :param exercises_client: Клиент для работы с API заданий.
        :param function_exercise: Фикстура созданного задания для удаления.
        """
        # Получаем ID задания из фикстуры
        exercise_id = function_exercise.response.exercise.id

        # Выполняем DELETE-запрос для удаления задания
        delete_response = exercises_client.delete_exercise_api(exercise_id)

        # Проверяем статус-код ответа на удаление
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        # Выполняем GET-запрос для проверки, что задание было удалено
        get_response = exercises_client.get_exercise_api(exercise_id)

        # Проверяем статус-код ответа на GET-запрос (404 - Not Found)
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)

        # Десериализуем JSON-ответ об ошибке в Pydantic-модель
        error_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)

        # Проверяем соответствие JSON-ответа схеме InternalErrorResponseSchema
        validate_json_schema(get_response.json(), error_response_data.model_json_schema())

        # Проверяем, что тело ответа содержит ошибку "Exercise not found"
        assert_exercise_not_found_response(error_response_data)