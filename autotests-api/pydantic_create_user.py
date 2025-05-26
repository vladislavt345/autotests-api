"""
Pydantic для работы с пользователями через API.

Модуль содержит схемы данных для эндпоинта POST /api/v1/users,
который используется для создания новых пользователей в системе.

Модели:
    - UserSchema: Базовая модель данных пользователя
    - CreateUserRequestSchema: Схема запроса на создание пользователя
    - CreateUserResponseSchema: Схема ответа с данными созданного пользователя
"""

from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    """
    Модель данных пользователя.
    
    Содержит в себе информацию: ID, email, fio.
    
    Attributes:
        id (str): Уникальный идентификатор пользователя
        email (EmailStr): Адрес электронной почты пользователя
        last_name (str): Фамилия пользователя
        first_name (str): Имя пользователя
        middle_name (str): Отчество пользователя
    """
    
    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")

    def get_full_name(self) -> str:
        """
        Возвращает полное имя пользователя.
        
        Returns:
            str: Полное имя в формате "Фамилия Имя Отчество"
        """
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()


class CreateUserRequestSchema(BaseModel):
    """
    Схема запроса на создание нового пользователя.
    
    Содержит в себе информацию: email, password, fio
    
    Attributes:
        email (EmailStr): Адрес электронной почты для регистрации
        password (str): Пароль для учетной записи
        last_name (str): Фамилия пользователя
        first_name (str): Имя пользователя
        middle_name (str): Отчество пользователя
    """
    
    email: EmailStr
    password: str
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")


class CreateUserResponseSchema(BaseModel):
    """
    Схема ответа на запрос создания пользователя.
    
    Содержит информацию:
    Успешно созданном пользователе.
    Возвращается сервером после успешной регистрации.
    
    Attributes:
        user (UserSchema): Данные созданного пользователя
    """
    
    user: UserSchema


# Пример использования моделей
if __name__ == "__main__":
    # Создание запроса на регистрацию пользователя
    create_request = CreateUserRequestSchema(
        email="john.doe@example.com",
        password="securePassword123",
        lastName="Doe",
        firstName="John",
        middleName="William"
    )
    
    print("Запрос на создание пользователя:")
    print(create_request.model_dump(by_alias=True))
    print()
    
    # Создание пользователя (имитация ответа от сервера)
    user_data = {
        "id": "user-12345",
        "email": "john.doe@example.com",
        "lastName": "Doe",
        "firstName": "John",
        "middleName": "William"
    }
    
    user = UserSchema(**user_data)
    print("Созданный пользователь:")
    print(user)
    print(f"Полное имя: {user.get_full_name()}")
    print()
    
    # Создание ответа сервера
    response = CreateUserResponseSchema(user=user)
    print("Ответ сервера:")
    print(response.model_dump(by_alias=True))
    
    # Пример работы с JSON
    json_response = """
    {
        "user": {
            "id": "user-67890",
            "email": "random.mail@example.com",
            "lastName": "String",
            "firstName": "Vladislav",
            "middleName": "String"
        }
    }
    """
    
    response_from_json = CreateUserResponseSchema.model_validate_json(json_response)
    print("\nОтвет, созданный из JSON:")
    print(f"ID пользователя: {response_from_json.user.id}")
    print(f"Email: {response_from_json.user.email}")
    print(f"Полное имя: {response_from_json.user.get_full_name()}")