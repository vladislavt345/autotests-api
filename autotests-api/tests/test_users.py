import pytest
from http import HTTPStatus
from src.schemas.users_schema import GetUserResponseSchema
from utils.assertions import assert_status_code, assert_get_user_response, validate_json_schema

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
    # GET-запрос к эндпоинту /api/v1/users/me
    response = private_users_client.get_user_me_api()
    
    # Преобразуем JSON-ответ в GetUserResponseSchema для валидации схемы
    response_data = GetUserResponseSchema.model_validate_json(response.text)
    
    # Проверка статус-код ответа
    assert_status_code(response.status_code, HTTPStatus.OK)
    
    # Проверка корректности тела ответа
    assert_get_user_response(response_data, function_user.response)

    # Валидация схемы ответа через json-schema
    validate_json_schema(response.json(), response_data.model_json_schema())