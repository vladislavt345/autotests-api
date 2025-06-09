from http import HTTPStatus

import pytest

from clients.users.private_users_client import PrivateUsersClient
from clients.users.public_users_client import PublicUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from tests.conftest import UserFixture
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response, assert_get_user_response


@pytest.mark.users
@pytest.mark.regression
def test_create_user(public_users_client: PublicUsersClient):
    """
    Тест проверяет создание нового пользователя через эндпоинт /api/v1/users.
    
    Проверяет:
    - Статус-код ответа (200)
    - Корректность тела ответа
    - Валидацию JSON schema ответа
    """

    # Формируем тело запроса на создание пользователя
    request = CreateUserRequestSchema()
    
    # Отправляем POST-запрос к эндпоинту создания пользователя
    response = public_users_client.create_user_api(request)
    
    # Преобразуем JSON-ответ в объект схемы CreateUserResponseSchema
    response_data = CreateUserResponseSchema.model_validate_json(response.text)

    # Проверка: статус-код должен быть 200 OK
    assert_status_code(response.status_code, HTTPStatus.OK)
    
    # Проверка: тело ответа соответствует данным запроса
    assert_create_user_response(request, response_data)

    # Валидация структуры и типов полей JSON-ответа по json-схеме Pydantic
    validate_json_schema(response.json(), response_data.model_json_schema())


@pytest.mark.users
@pytest.mark.regression
def test_get_user_me(function_user: UserFixture, private_users_client: PrivateUsersClient):
    """
    Тест проверяет получение данных текущего пользователя через эндпоинт /api/v1/users/me.
    
    Проверяет:
    - Статус-код ответа (200)
    - Корректность тела ответа
    - Валидацию JSON schema ответа
    """

    # Выполняем GET-запрос к эндпоинту /api/v1/users/me
    response = private_users_client.get_user_me_api()
    
    # Преобразуем JSON-ответ в объект схемы GetUserResponseSchema
    response_data = GetUserResponseSchema.model_validate_json(response.text)

    # Проверка: статус-код должен быть 200 OK
    assert_status_code(response.status_code, HTTPStatus.OK)
    
    # Проверка: содержимое ответа соответствует данным зарегистрированного пользователя
    assert_get_user_response(response_data, function_user.response)

    # Валидация структуры и типов полей JSON-ответа по json-схеме Pydantic
    validate_json_schema(response.json(), response_data.model_json_schema())