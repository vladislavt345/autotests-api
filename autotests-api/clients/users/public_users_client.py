from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient

class CreateUserRequestDict(TypedDict):
    """
    Описание структуры запроса для создания пользователя.
    """
    id: str
    email: str
    password: str
    lastName: str
    firstName: str
    middleName: str

class PublicUsersClient(APIClient):
    """
    Клиент для работы с публичными методами API /api/v1/users
    (методами, не требующими авторизации)
    """

    def create_user_api(self, request: CreateUserRequestDict) -> Response:
        """
        Метод создает нового пользователя через API.

        :param request: Словарь с данными пользователя в формате:
            {
                "id": "string",
                "email": "user@example.com",
                "lastName": "string",
                "firstName": "string",
                "middleName": "string"
            }
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post("/api/v1/users", json=request)