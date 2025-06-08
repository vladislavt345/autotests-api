import pytest
from pydantic import BaseModel, EmailStr
from clients.authentication.authentication_client import AuthenticationClient, get_authentication_client
from clients.users.public_users_client import get_public_users_client, PublicUsersClient
from clients.users.private_users_client import get_private_users_client, PrivateUsersClient
from clients.private_http_builder import AuthenticationUserSchema
# Импортируем запрос и ответ создания пользователя
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema

# Модель для агрегации возвращаемых данных фикстурой function_user
class UserFixture(BaseModel):
    request: CreateUserRequestSchema
    response: CreateUserResponseSchema
    
    @property
    def email(self) -> EmailStr:  # Быстрый доступ к email пользователя
        return self.request.email
    
    @property
    def password(self) -> str:  # Быстрый доступ к password пользователя
        return self.request.password
    
    @property
    def authentication_user(self) -> AuthenticationUserSchema:
        """Возвращает данные для аутентификации API-клиентов"""
        return AuthenticationUserSchema(
            email=self.email,
            password=self.password
        )

@pytest.fixture
def authentication_client() -> AuthenticationClient:
    return get_authentication_client()

@pytest.fixture
def public_users_client() -> PublicUsersClient:
    return get_public_users_client()

@pytest.fixture
def private_users_client(function_user: UserFixture) -> PrivateUsersClient:
    """
    Фикстура для создания приватного клиента пользователей с аутентификацией.
    :param function_user: Фикстура с данными созданного пользователя.
    :return: Инициализированный PrivateUsersClient.
    """
    return get_private_users_client(function_user.authentication_user)

# Фикстура для создания пользователя
@pytest.fixture
# Используем фикстуру public_users_client, которая создает нужный API клиент
def function_user(public_users_client: PublicUsersClient) -> UserFixture:
    request = CreateUserRequestSchema()
    response = public_users_client.create_user(request)
    return UserFixture(request=request, response=response)  # Возвращаем все нужные данные