from typing import TypedDict
import httpx

from clients.api_client import APIClient


class UserCreateRequest(TypedDict):
    """
    TypedDict для запроса на создание пользователя.

    Attributes:
        id: Идентификатор пользователя.
        email: Email пользователя.
        password: Пароль пользователя.
        lastName: Фамилия пользователя.
        firstName: Имя пользователя.
        middleName: Отчество пользователя.
    """
    id: str
    email: str
    password: str
    lastName: str
    firstName: str
    middleName: str


class PublicUsersClient(APIClient):
    """
    Клиент для взаимодействия с публичными методами API пользователей.
    
    Работает с эндпоинтами, которые не требуют авторизации, такими как
    создание нового пользователя.
    """
    
    def create_user_api(self, request: UserCreateRequest) -> httpx.Response:
        """
        Выполняет POST-запрос к API для создания нового пользователя.
        
        Args:
            request: Данные для создания пользователя, включающие
                login, password и email.
                
        Returns:
            httpx.Response: Ответ от API сервера, содержащий информацию о
            результате создания пользователя.
            
        Example:
            >>> client = PublicUsersClient(base_url="https://api.example.com")
            >>> response = client.create_user_api({
            ...     "id": "user123",
            ...     "email": "user@example.com",
            ...     "password": "securepass",
            ...     "lastName": "Иванов",
            ...     "firstName": "Иван",
            ...     "middleName": "Иванович"
            ... })
        """
        return self.client.post("/api/v1/users", json=request)