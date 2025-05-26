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
    
    Содержит в себе атрибуты: email, password, fio
    
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
    
    Содержит информацию о успешно созданном пользователе.
    Возвращается сервером после успешной регистрации.
    
    Attributes:
        user (UserSchema): Данные созданного пользователя
    """
    
    user: UserSchema