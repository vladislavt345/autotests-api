from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    GetExerciseResponseSchema,
    UpdateExerciseRequestSchema,
    UpdateExerciseResponseSchema,
    GetExercisesQuerySchema,
    GetExercisesResponseSchema
)
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.allure.epics import AllureEpic  # Импортируем enum AllureEpic
from tools.allure.features import AllureFeature  # Импортируем enum AllureFeature
from tools.allure.stories import AllureStory  # Импортируем enum AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import (
    assert_create_exercise_response,
    assert_get_exercise_response,
    assert_update_exercise_response,
    assert_exercise_not_found_response,
    assert_get_exercises_response
)
from tools.assertions.schema import validate_json_schema


@pytest.mark.exercises
@pytest.mark.regression
@allure.tag(AllureTag.EXERCISES, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.EXERCISES)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.EXERCISES)
class TestExercises:
    """
    Тестовый класс для проверки функциональности API заданий.
    """

    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.title("Create exercise")
    @allure.severity(Severity.BLOCKER)
    def test_create_exercise(
            self,
            function_course: CourseFixture,
            exercises_client: ExercisesClient
    ):
        """
        Тест создания задания через POST-запрос к /api/v1/exercises.

        Проверяет:
        - Статус-код ответа 200
        - Соответствие тела ответа запросу
        - Валидацию JSON schema ответа
        """
        request = CreateExerciseRequestSchema(course_id=function_course.response.course.id)
        response = exercises_client.create_exercise_api(request)
        assert_status_code(response.status_code, HTTPStatus.OK)
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)
        assert_create_exercise_response(request, response_data)
        
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureStory.GET_ENTITY)
    @allure.title("Get exercise")
    @allure.severity(Severity.BLOCKER)
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
        """
        exercise_id = function_exercise.response.exercise.id
        response = exercises_client.get_exercise_api(exercise_id)
        assert_status_code(response.status_code, HTTPStatus.OK)
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)
        assert_get_exercise_response(response_data, function_exercise.response)
        
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    @allure.title("Update exercise")
    @allure.severity(Severity.CRITICAL)
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
        """
        exercise_id = function_exercise.response.exercise.id
        request = UpdateExerciseRequestSchema()
        response = exercises_client.update_exercise_api(exercise_id, request)
        assert_status_code(response.status_code, HTTPStatus.OK)
        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)
        assert_update_exercise_response(request, response_data)
        
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.title("Delete exercise")
    @allure.severity(Severity.CRITICAL)
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
        """
        exercise_id = function_exercise.response.exercise.id
        delete_response = exercises_client.delete_exercise_api(exercise_id)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        get_response = exercises_client.get_exercise_api(exercise_id)
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        get_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)
        assert_exercise_not_found_response(get_response_data)
        
        validate_json_schema(get_response.json(), get_response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    @allure.title("Get exercises")
    @allure.severity(Severity.BLOCKER)
    def test_get_exercises(
            self,
            exercises_client: ExercisesClient,
            function_course: CourseFixture,
            function_exercise: ExerciseFixture
    ):
        """
        Тест получения списка заданий через GET-запрос к /api/v1/exercises.

        Проверяет:
        - Статус-код ответа 200
        - Соответствие тела ответа списку созданных заданий
        - Валидацию JSON schema ответа
        """
        query = GetExercisesQuerySchema(course_id=function_course.response.course.id)
        response = exercises_client.get_exercises_api(query)
        assert_status_code(response.status_code, HTTPStatus.OK)
        response_data = GetExercisesResponseSchema.model_validate_json(response.text)
        assert_get_exercises_response(response_data, [function_exercise.response])
        
        validate_json_schema(response.json(), response_data.model_json_schema())