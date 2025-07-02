from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.users.private_users_client import PrivateUsersClient
from clients.users.public_users_client import PublicUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from fixtures.users import UserFixture
from tools.allure.epics import AllureEpic  # Импортируем enum AllureEpic
from tools.allure.features import AllureFeature  # Импортируем enum AllureFeature
from tools.allure.stories import AllureStory  # Импортируем enum AllureStory
from tools.allure.tags import AllureTag  # Используем enum
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response, assert_get_user_response
from tools.fakers import fake


@pytest.mark.users
@pytest.mark.regression
@allure.tag(AllureTag.USERS, AllureTag.REGRESSION)  # Теги для класса через enum
@allure.epic(AllureEpic.LMS)  # Добавили epic
@allure.feature(AllureFeature.USERS)  # Добавили feature
@allure.parent_suite(AllureEpic.LMS)  # Добавили parent_suite_epic
@allure.suite(AllureFeature.USERS)  # Добавили suite_feature
class TestUsers:

    @pytest.mark.parametrize("email", ["mail.ru", "gmail.com", "example.com"])
    @allure.tag(AllureTag.CREATE_ENTITY)  # Тег через enum
    @allure.story(AllureStory.CREATE_ENTITY)  # Добавили story
    @allure.sub_suite(AllureStory.CREATE_ENTITY)  # Добавили sub_suite_story
    @allure.title("Create user")
    @allure.severity(Severity.BLOCKER)
    def test_create_user(self, email: str, public_users_client: PublicUsersClient):
        """
        Тест проверяет создание нового пользователя через эндпоинт /api/v1/users.

        Проверяет:
        - Статус-код ответа (200)
        - Корректность тела ответа
        - Валидацию JSON schema ответа
        """
        request = CreateUserRequestSchema(email=fake.email(domain=email))
        response = public_users_client.create_user_api(request)
        response_data = CreateUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_user_response(request, response_data)
        
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITY)  # Тег через enum
    @allure.story(AllureStory.GET_ENTITY)  # Добавили story
    @allure.sub_suite(AllureStory.GET_ENTITY)  # Добавили sub_suite_story
    @allure.title("Get user me")
    @allure.severity(Severity.CRITICAL)
    def test_get_user_me(self, function_user: UserFixture, private_users_client: PrivateUsersClient):
        """
        Тест проверяет получение данных текущего пользователя через эндпоинт /api/v1/users/me.

        Проверяет:
        - Статус-код ответа (200)
        - Корректность тела ответа
        - Валидацию JSON schema ответа
        """
        response = private_users_client.get_user_me_api()
        response_data = GetUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_user_response(response_data, function_user.response)
        
        validate_json_schema(response.json(), response_data.model_json_schema())