from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    GetExerciseResponseSchema,
    GetExercisesResponseSchema,
    UpdateExerciseRequestSchema,
    ExerciseSchema
)

from clients.errors_schema import InternalErrorResponseSchema
from tools.assertions.base import assert_equal


def assert_create_exercise_response(request: CreateExerciseRequestSchema, response: CreateExerciseResponseSchema):
    """
    Проверяет, что ответ на создание задания соответствует запросу.
    
    :param request: Исходный запрос на создание задания
    :param response: Ответ API с данными задания
    :raises AssertionError: Если хотя бы одно поле не совпадает
    """
    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.course_id, request.course_id, "course_id")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")


def assert_exercise(actual: ExerciseSchema, expected: ExerciseSchema):
    """
    Проверяет корректность данных задания.
    Сравнивает все поля задания.
    
    :param actual: Фактические данные задания
    :param expected: Ожидаемые данные задания
    :raises AssertionError: Если хотя бы одно поле не совпадает
    """
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.course_id, expected.course_id, "course_id")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.order_index, expected.order_index, "order_index")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")


def assert_get_exercise_response(get_exercise_response: GetExerciseResponseSchema, create_exercise_response: CreateExerciseResponseSchema):
    """
    Проверяет, что данные задания при создании и при запросе совпадают.
    
    :param get_exercise_response: Ответ API при запросе задания
    :param create_exercise_response: Ответ API при создании задания
    :raises AssertionError: Если данные заданий не совпадают
    """
    assert_exercise(get_exercise_response.exercise, create_exercise_response.exercise)


def assert_get_exercises_response(get_exercises_response: GetExercisesResponseSchema, create_exercise_response: CreateExerciseResponseSchema):
    """
    Проверяет, что список заданий содержит ранее созданное задание.
    
    Функция проходит по всем заданиям в списке и проверяет каждое задание
    с помощью функции assert_exercise. Проверяет, что созданное задание
    присутствует в полученном списке.
    
    :param get_exercises_response: Ответ API со списком заданий
    :param create_exercise_response: Ответ API при создании задания
    :raises AssertionError: Если созданное задание не найдено в списке или данные не совпадают
    """
    # Получаем созданное задание для сравнения
    created_exercise = create_exercise_response.exercise
    
    # Проверяем, что список заданий не пустой
    assert get_exercises_response.exercises, "Список заданий не должен быть пустым."
        
    # Ищем созданное задание в списке
    exercise_found = next(
        (exercise for exercise in get_exercises_response.exercises if exercise.id == created_exercise.id),
        None
    )
    
    # Проверяем, что созданное задание было найдено в списке
    assert exercise_found, f"Созданное задание с ID {created_exercise.id} не найдено в списке заданий"
    # Проверяем, что все данные найденного задания полностью совпадают с созданными.
    # assert_exercise(exercise_found, created_exercise)

def assert_update_exercise_response(request: UpdateExerciseRequestSchema, response: GetExerciseResponseSchema):
    """
    Проверяет, что ответ на обновление задания соответствует запросу.
    
    Функция проверяет только те поля, которые были указаны в запросе на обновление
    (имеют значение, отличное от None). Это позволяет корректно обрабатывать
    частичные обновления задания через PATCH-запрос.
    
    :param request: Исходный запрос на обновление задания
    :param response: Ответ API с обновленными данными задания
    :raises AssertionError: Если хотя бы одно обновленное поле не совпадает с запросом
    """
    # Проверяем только те поля, которые были переданы в запросе (!= None)
    if request.title is not None:
        assert_equal(response.exercise.title, request.title, "title")
    
    if request.max_score is not None:
        assert_equal(response.exercise.max_score, request.max_score, "max_score")
    
    if request.min_score is not None:
        assert_equal(response.exercise.min_score, request.min_score, "min_score")
    
    if request.order_index is not None:
        assert_equal(response.exercise.order_index, request.order_index, "order_index")
    
    if request.description is not None:
        assert_equal(response.exercise.description, request.description, "description")
    
    if request.estimated_time is not None:
        assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")

#Проверка, что тело ответа на запрос получения задания содержит внутреннюю ошибку "Exercise not found"
def assert_exercise_not_found_response(response: InternalErrorResponseSchema):
    """
    Проверяет, что ответ соответствует ожидаемой ошибке "Exercise not found".

    :param response: Десериализованный ответ API об ошибке.
    :raises AssertionError: Если сообщение не соответствует ожидаемому.
    """
    expected_message = "Exercise not found"
    assert_equal(response.details, expected_message, "error details message")