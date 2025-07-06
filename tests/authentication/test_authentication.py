from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity  # Импортируем enum Severity из Allure

from clients.authentication.authentication_client import AuthenticationClient
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from clients.users.public_users_client import PublicUsersClient
from fixtures.users import UserFixture
from tools.allure.epics import AllureEpic  # Импортируем enum AllureEpic
from tools.allure.features import AllureFeature  # Импортируем enum AllureFeature
from tools.allure.stories import AllureStory  # Импортируем enum AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.authentication import assert_login_response
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema


@pytest.mark.regression
@pytest.mark.authentication
@allure.tag(AllureTag.REGRESSION, AllureTag.AUTHENTICATION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.AUTHENTICATION)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.AUTHENTICATION)
class TestAuthentication:
    @allure.story(AllureStory.LOGIN)
    @allure.sub_suite(AllureStory.LOGIN)
    @allure.title("Login with correct email and password")
    @allure.severity(Severity.BLOCKER)
    def test_login(
        self,
        function_user: UserFixture,
        authentication_client: AuthenticationClient
    ):
        """
        Тест проверяет авторизацию пользователя через эндпоинт /api/v1/auth/login.
        
        Проверяет:
        - Статус-код (200 OK)
        - Корректность данных авторизации
        - Валидацию JSON-схемы ответа
        """

        # Формируем запрос авторизации на основе данных созданного пользователя
        request = LoginRequestSchema(
            email=function_user.email,
            password=function_user.password
        )

        # Выполняем авторизацию пользователя
        response = authentication_client.login_api(request)

        # Преобразуем ответ в объект схемы
        response_data = LoginResponseSchema.model_validate_json(response.text)

        # Проверка: статус-код
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Проверка: содержимое ответа (access_token и т. д.)
        assert_login_response(response_data)

        # Валидация структуры JSON-ответа по JSON-схеме
        validate_json_schema(response.json(), response_data.model_json_schema())