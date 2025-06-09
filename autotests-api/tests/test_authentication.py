from http import HTTPStatus

import pytest

from clients.authentication.authentication_client import AuthenticationClient
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from tests.conftest import UserFixture
from tools.assertions.authentication import assert_login_response
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema


@pytest.mark.regression  # Добавил маркировку regression
@pytest.mark.authentication  # Добавил маркировку authentication
def test_login(
        function_user: UserFixture,  # Используем фикстуру для создания пользователя
        authentication_client: AuthenticationClient
):
    """
    Тест проверяет авторизацию пользователя.
    """

    """
    Функция формирует запрос авторизации на основе данных созданного пользователя.
    :param: login_request с учетными данными пользователя.
    """
    request = LoginRequestSchema(email=function_user.email, password=function_user.password)

    """
    Функция выполняет авторизацию пользователя.
    :param: login_request с учетными данными пользователя.
    :return: HTTP ответ с результатом авторизации.
    """
    response = authentication_client.login_api(request)
    response_data = LoginResponseSchema.model_validate_json(response.text)

    """
    Функции выполняют проверки ответа авторизации.
    :return: валидация статус кода, данных авторизации и JSON схемы.
    """
    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_login_response(response_data)
    
    # Валидация схемы ответа через json-schema
    validate_json_schema(response.json(), response_data.model_json_schema())