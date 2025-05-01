from typing import Any
from httpx import Client, URL, Response, QueryParams
from httpx._types import RequestData, RequestFiles


class APIClient:
    """
    Базовый клиент для работы с API.
    Предоставляет основные методы для выполнения HTTP-запросов.
    Наследуется специализированными API-клиентами.
    """

    def __init__(self, client: Client) -> None:
        """
        Инициализация базового API клиента.

        Args:
            client: Экземпляр httpx.Client для выполнения HTTP-запросов.
                   Должен быть предварительно сконфигурирован (base_url, timeout и т.д.)
        """
        self.client = client

    def get(self, url: URL | str, params: QueryParams | None = None) -> Response:
        """
        Выполняет GET-запрос к указанному эндпоинту.

        Args:
            url: URL или относительный путь эндпоинта
            params: Опциональные query-параметры запроса

        Returns:
            httpx.Response: Объект ответа от сервера
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
        Выполняет POST-запрос с возможностью отправки разных типов данных.

        Args:
            url: URL или относительный путь эндпоинта
            json: Данные для отправки в формате JSON
            data: Данные для отправки в формате form-data
            files: Файлы для загрузки на сервер

        Returns:
            httpx.Response: Объект ответа от сервера
        """
        return self.client.post(url, json=json, data=data, files=files)

    def patch(self, url: URL | str, json: Any | None = None) -> Response:
        """
        Выполняет PATCH-запрос для частичного обновления ресурса.

        Args:
            url: URL или относительный путь эндпоинта
            json: Данные для частичного обновления в формате JSON

        Returns:
            httpx.Response: Объект ответа от сервера
        """
        return self.client.patch(url, json=json)

    def delete(self, url: URL | str) -> Response:
        """
        Выполняет DELETE-запрос для удаления ресурса.

        Args:
            url: URL или относительный путь эндпоинта

        Returns:
            httpx.Response: Объект ответа от сервера
        """
        return self.client.delete(url)