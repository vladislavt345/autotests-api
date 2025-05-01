import httpx

# URL для запросов
login_url = "http://localhost:8000/api/v1/authentication/login"
user_url = "http://localhost:8000/api/v1/users/me"

# Данные для авторизации
login_data = {
    "email": "TestName@example.com",
    "password": "321321"
}

# 1.POST-запрос
# Отправляем запрос авторизации
login_response = httpx.post(login_url, json=login_data)
print(f"Код ответа при получении токена: {login_response.status_code}")
print(login_response.json())

# 2.GET-запрос
# Извлекаем токен из ответа
token_data = login_response.json()
access_token = token_data["token"]["accessToken"]

# Передаем заголовок
headers = {
    "Authorization": f"Bearer {access_token}" #{access_token}
}

# Отправляем GET-запрос с токеном авторизации
user_response = httpx.get(user_url, headers=headers)

# Выводим данные пользователя и код статуса
print(f"Код ответа при запросе данных пользователя: {user_response.status_code}")
print("Данные пользователя:")
print(user_response.json())