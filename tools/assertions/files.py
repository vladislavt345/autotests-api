import allure

from clients.errors_schema import (
    InternalErrorResponseSchema,
    ValidationErrorResponseSchema,
    ValidationErrorSchema,
)

from clients.files.files_schema import (
    CreateFileRequestSchema,
    CreateFileResponseSchema,
    FileSchema,
    GetFileResponseSchema,
)

from config import settings

from tools.assertions.base import assert_equal

from tools.assertions.errors import (
    assert_internal_error_response,
    assert_validation_error_response,
)

from tools.logger import get_logger
logger = get_logger("FILES_ASSERTIONS")

@allure.step("Check create file response")
def assert_create_file_response(request: CreateFileRequestSchema, response: CreateFileResponseSchema):
    """
    Проверяет, что ответ на создание файла соответствует запросу.

    :param request: Исходный запрос на создание файла.
    :param response: Ответ API с данными файла.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    # Логируем факт начала проверки
    logger.info("Check create file response")
    # Формируем ожидаемую ссылку на загруженный файл
    expected_url = f"{settings.http_client.client_url}static/{request.directory}/{request.filename}"

    assert_equal(str(response.file.url), expected_url, "url")
    assert_equal(response.file.filename, request.filename, "filename")
    assert_equal(response.file.directory, request.directory, "directory")

def assert_file_is_accessible(url: str):
    """
    Проверяет, что файл доступен по указанному URL.
    
    :param url: Ссылка на файл.
    :raises AssertionError: Если файл не доступен.
    """
    import httpx
    
    response = httpx.get(url)
    assert response.status_code == 200, f"Файл недоступен по URL: {url}"\
        
@allure.step("Check file")
def assert_file(actual: FileSchema, expected: FileSchema):
    """
    Проверяет, что фактические данные файла соответствуют ожидаемым.

    :param actual: Фактические данные файла.
    :param expected: Ожидаемые данные файла.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    # Логируем факт начала проверки
    logger.info("Check file")
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.url, expected.url, "url")
    assert_equal(actual.filename, expected.filename, "filename")
    assert_equal(actual.directory, expected.directory, "directory")

@allure.step("Check get file response")  # Добавили allure шаг
def assert_get_file_response(
        get_file_response: GetFileResponseSchema,
        create_file_response: CreateFileResponseSchema
):
    """
    Проверяет, что ответ на получение файла соответствует ответу на его создание.

    :param get_file_response: Ответ API при запросе данных файла.
    :param create_file_response: Ответ API при создании файла.
    :raises AssertionError: Если данные файла не совпадают.
    """
    logger.info("Check get file response")
    assert_file(get_file_response.file, create_file_response.file)
    
@allure.step("Check create file with empty filename response")
def assert_create_file_with_empty_filename_response(actual: ValidationErrorResponseSchema):
    """
    Проверяет, что ответ на создание файла с пустым именем файла соответствует ожидаемой валидационной ошибке.

    :param actual: Ответ от API с ошибкой валидации, который необходимо проверить.
    :raises AssertionError: Если фактический ответ не соответствует ожидаемому.
    """
    logger.info("Check create file with empty filename response")
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="string_too_short",  # Тип ошибки, связанной с слишком короткой строкой.
                input="",  # Пустое имя файла.
                context={"min_length": 1},  # Минимальная длина строки должна быть 1 символ.
                message="String should have at least 1 character",  # Сообщение об ошибке.
                location=["body", "filename"]  # Ошибка возникает в теле запроса, поле "filename".
            )
        ]
    )
    assert_validation_error_response(actual, expected)

@allure.step("Check create file with empty directory response")
def assert_create_file_with_empty_directory_response(actual: ValidationErrorResponseSchema):
    """
    Проверяет, что ответ на создание файла с пустым значением директории соответствует ожидаемой валидационной ошибке.

    :param actual: Ответ от API с ошибкой валидации, который необходимо проверить.
    :raises AssertionError: Если фактический ответ не соответствует ожидаемому.
    """
    logger.info("Check create file with empty directory response")
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="string_too_short",  # Тип ошибки, связанной с слишком короткой строкой.
                input="",  # Пустая директория.
                context={"min_length": 1},  # Минимальная длина строки должна быть 1 символ.
                message="String should have at least 1 character",  # Сообщение об ошибке.
                location=["body", "directory"]  # Ошибка возникает в теле запроса, поле "directory".
            )
        ]
    )
    assert_validation_error_response(actual, expected)

@allure.step("Check get file with incorrect file id response")
def assert_get_file_with_incorrect_file_id_response(actual: ValidationErrorResponseSchema):
    """
    Проверяет, что ответ на получение файла с некорректным file_id соответствует ожидаемой валидационной ошибке.

    :param actual: Ответ от API с ошибкой валидации, который необходимо проверить.
    :raises AssertionError: Если фактический ответ не соответствует ожидаемому.
    """
    # Логируем факт начала проверки
    logger.info("Check get file with incorrect file id response")
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="uuid_parsing",  # Тип ошибки, связанной с парсингом UUID.
                input="incorrect-file-id",  # Некорректный file_id.
                context={
                    "error": "invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1"
                },  # Контекст ошибки с подробным описанием.
                message="Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1",  # Сообщение об ошибке.
                location=["path", "file_id"]  # Ошибка возникает в пути запроса, параметр "file_id".
            )
        ]
    )
    assert_validation_error_response(actual, expected)

@allure.step("Check file not found response")
def assert_file_not_found_response(actual: InternalErrorResponseSchema):
    """
    Функция для проверки ошибки, если файл не найден на сервере.

    :param actual: Фактический ответ.
    :raises AssertionError: Если фактический ответ не соответствует ошибке "File not found"
    """
    # Логируем факт начала проверки
    logger.info("Check file not found response")
    # Ожидаемое сообщение об ошибке, если файл не найден
    expected = InternalErrorResponseSchema(details="File not found")
    # Используем ранее созданную функцию для проверки внутренней ошибки
    assert_internal_error_response(actual, expected)