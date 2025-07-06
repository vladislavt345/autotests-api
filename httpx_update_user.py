import httpx
from tools.fakers import fake

# 1. Создание пользователя
create_user_payload = {
    "email": get_random_email(),
    "password": "string",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
}

with httpx.Client() as client:
    # Создаем пользователя
    create_user_response = client.post(
        "http://localhost:8000/api/v1/users",
        json=create_user_payload
    )
    create_user_response_data = create_user_response.json()
    print('Create user status:', create_user_response.status_code)
    print('Create user data:', create_user_response_data)

    # 2. Авторизация пользователя
    login_payload = {
        "email": create_user_payload["email"],
        "password": create_user_payload["password"]
    }

    login_response = client.post(
        "http://localhost:8000/api/v1/authentication/login",
        json=login_payload
    )
    login_response_data = login_response.json()
    print('\nLogin status:', login_response.status_code)
    print('Login data:', login_response_data)

    # 3. Обновление данных пользователя
    update_user_headers = {
        "Authorization": f"Bearer {login_response_data['token']['accessToken']}"
    }

    update_user_payload = {
        "email": get_random_email(),  # Генерируем новый email
        "lastName": "updatedLastName",
        "firstName": "updatedFirstName",
        "middleName": "updatedMiddleName"
    }

    update_user_response = client.patch(
        f"http://localhost:8000/api/v1/users/{create_user_response_data['user']['id']}",
        json=update_user_payload,
        headers=update_user_headers
    )
    update_user_response_data = update_user_response.json()
    print('\nUpdate user status:', update_user_response.status_code)
    print('Updated user data:', update_user_response_data)