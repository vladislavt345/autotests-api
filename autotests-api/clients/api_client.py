from typing import Any
from httpx import Client, URL, Response, QueryParams
from httpx._types import RequestData, RequestFiles

class APIClient:
    def __init__(self, client: Client):
        """
        Базовый API клиент, обёртка над httpx.Client.

        :param client: Экземпляр httpx.Client с предустановленной конфигурацией (например, заголовки, авторизация).
        """
        self.client = client

    def get(self, url: URL | str, params: QueryParams | None = None) -> Response:
        """
        Выполняет GET-запрос.

        :param url: URL-адрес эндпоинта.
        :param params: GET-параметры запроса (например, ?key=value).
        :return: Объект Response с данными ответа.
        """
        return self.client.get(url, params=params)

    def post(
        self,
        url: URL | str,
        json: Any | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None
    ) -> Response:
        """
        Выполняет POST-запрос.

        :param url: URL-адрес эндпоинта.
        :param json: Данные в формате JSON.
        :param data: Форматированные данные формы.
        :param files: Файлы для загрузки на сервер.
        :return: Объект Response с данными ответа.
        """
        return self.client.post(url, json=json, data=data, files=files)

    def patch(
        self,
        url: URL | str,
        json: Any | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None
    ) -> Response:
        """
        Выполняет PATCH-запрос.

        :param url: URL-адрес эндпоинта.
        :param json: Данные в формате JSON.
        :param data: Форматированные данные формы.
        :param files: Файлы для загрузки.
        :return: Объект Response с данными ответа.
        """
        return self.client.patch(url, json=json, data=data, files=files)

    def delete(self, url: URL | str) -> Response:
        """
        Выполняет DELETE-запрос.

        :param url: URL-адрес ресурса для удаления.
        :return: Объект Response с данными ответа.
        """
        return self.client.delete(url)