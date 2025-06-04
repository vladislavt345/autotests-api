from clients.users.public_users_client import get_public_users_client
from clients.users.private_users_client import get_private_users_client
from clients.users.users_schema import CreateUserRequestSchema, GetUserResponseSchema
from tools.assertions.schema import validate_json_schema
from tools.fakers import get_random_email

# Создаём публичный ю.клиент
public_users_client = get_public_users_client()

# 1. Создаём пользователя
user_data = CreateUserRequestSchema(
    email=get_random_email(),
    password="string",
    last_name="string",
    first_name="string",
    middle_name="string"
)

print("Создаём пользователя...")
create_resp = public_users_client.create_user_api(user_data)
user_id = create_resp.json()['user']['id']
print(f"Пользователь создан. ID: {user_id}")

# 2. Авторизуемся как пользователь (приватный ю.клиент)
print("Авторизуемся как пользователь...")
private_users_client = get_private_users_client(user_data)
print("Авторизация прошла успешно")

# 3. Получаем информацию о пользователе
print(f"Получаем данные пользователя с ID {user_id}...")
get_user_resp = private_users_client.get_user_api(user_id)
print("Данные получены")

# 4. Готовим схему и валидируем ответ
schema = GetUserResponseSchema.model_json_schema()
print("Проверяем структуру на соотвествие ответу")

try:
    validate_json_schema(instance=get_user_resp.json(), schema=schema)
    print("Ответ соответствует схеме.")
except Exception as e:
    print(f"Ошибка валидации: {e}")
    raise

# Вывод результа
print("\nСкрипт выполнен успешно")
print("Результат:")
print(get_user_resp.json())