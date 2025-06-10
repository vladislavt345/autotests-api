import pytest
from pydantic import BaseModel
from clients.exercises.exercises_client import ExercisesClient, get_exercises_client
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from fixtures.users import UserFixture
from fixtures.courses import CourseFixture


class ExerciseFixture(BaseModel):
    request: CreateExerciseRequestSchema
    response: CreateExerciseResponseSchema


@pytest.fixture
def exercises_client(function_user: UserFixture) -> ExercisesClient:
    """
    Фикстура для создания экземпляра API-клиента ExercisesClient.
    
    :param function_user: Фикстура пользователя для аутентификации
    :return: Готовый к использованию ExercisesClient
    """
    return get_exercises_client(function_user.authentication_user)


@pytest.fixture
def function_exercise(
        exercises_client: ExercisesClient,
        function_course: CourseFixture
) -> ExerciseFixture:
    """
    Фикстура для создания тестового задания.
    
    :param exercises_client: Клиент для работы с API заданий
    :param function_course: Фикстура курса для связи с заданием
    :return: Объект ExerciseFixture с данными запроса и ответа
    """
    request = CreateExerciseRequestSchema(
        course_id=function_course.response.course.id
    )
    response = exercises_client.create_exercise(request)
    return ExerciseFixture(request=request, response=response)