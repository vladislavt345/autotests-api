import allure
from httpx import Response

from clients.api_client import APIClient
from clients.api_coverage import tracker
from clients.public_http_builder import get_public_http_client
from clients.users.users_schema import CreateUserResponseSchema, CreateUserRequestSchema
from tools.routes import APIRoutes

class PublicUsersClient(APIClient):
    """
    Клиент для работы с /api/v1/users
    """

    @allure.step("Create user")
    # Cбор покрытия для эндпоинта POST /api/v1/users
    @tracker.track_coverage_httpx(APIRoutes.USERS)
    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        """
        Метод создает пользователя.

        :param request: Словарь с email, password, lastName, firstName, middleName.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post(APIRoutes.USERS, json=request.model_dump(by_alias=True))

    def create_user(self, request: CreateUserRequestSchema) -> CreateUserResponseSchema:
        response = self.create_user_api(request)
        return CreateUserResponseSchema.model_validate_json(response.text)


def get_public_users_client() -> PublicUsersClient:
    """
    Функция создаёт экземпляр PublicUsersClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию PublicUsersClient.
    """
    return PublicUsersClient(client=get_public_http_client())