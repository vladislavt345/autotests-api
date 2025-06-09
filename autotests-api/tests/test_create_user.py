from http import HTTPStatus

import pytest

from clients.users.public_users_client import PublicUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response
from tools.fakers import fake


@pytest.mark.users
@pytest.mark.regression
@pytest.mark.parametrize("domain", ["mail.ru", "gmail.com", "example.com"])
def test_create_user(domain: str, public_users_client: PublicUsersClient):
    """
    Тест создания пользователя с параметризованным доменом email.
    
    :param domain: Домен электронной почты для тестирования
    :param public_users_client: Фикстура API клиента
    """
    # Создаем email с указанным доменом
    email = fake.email(domain=domain)
    
    # Создаем запрос с параметризованным email
    request = CreateUserRequestSchema(email=email)
    
    response = public_users_client.create_user_api(request)
    response_data = CreateUserResponseSchema.model_validate_json(response.text)
    
    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_create_user_response(request, response_data)
    validate_json_schema(response.json(), response_data.model_json_schema())