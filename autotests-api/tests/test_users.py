from http import HTTPStatus
import pytest
from clients.users.private_users_client import PrivateUsersClient
from clients.users.users_schema import GetUserResponseSchema
from tests.conftest import UserFixture
from tools.assertions.base import assert_status_code
from tools.assertions.users import assert_get_user_response

@pytest.mark.users
@pytest.mark.regression
def test_get_user_me(private_users_client: PrivateUsersClient, function_user: UserFixture):
    """
    Тест проверяет получение данных текущего пользователя через эндпоинт /api/v1/users/me.
    
    Проверяет:
    - Статус-код ответа (200)
    - Корректность тела ответа
    - Валидацию JSON schema ответа
    """
    # Выполняем GET-запрос к эндпоинту /api/v1/users/me
    response = private_users_client.get_user_me_api()
    
    # Проверяем статус-код ответа
    assert_status_code(response.status_code, HTTPStatus.OK)
    
    # Преобразуем JSON-ответ в GetUserResponseSchema для валидации схемы
    get_user_response = GetUserResponseSchema.model_validate_json(response.text)
    
    # Проверяем корректность тела ответа
    assert_get_user_response(get_user_response, function_user.response)