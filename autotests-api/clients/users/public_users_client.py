from typing import TypedDict, NotRequired
from httpx import Response

from clients.api_client import APIClient

class CreateUserRequestDict(TypedDict):
    """
    Описание структуры запроса на создание пользователя.
    """
    email: str
    password: str
    lastName: str
    firstName: str
    middleName: str

class PublicUsersClient(APIClient):
    """
    Клиент для публичных методов /api/v1/users.
    Используется для создания пользователей без авторизации.
    """

    def create_user_api(self, request: CreateUserRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания нового пользователя.

        :param request: Словарь с данными пользователя (email, password, firstName, lastName, middleName.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post("/api/v1/users", json=request)