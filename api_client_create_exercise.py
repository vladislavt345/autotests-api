from clients.courses.courses_client import get_courses_client
from clients.courses.courses_schema import CreateCourseRequestSchema
from clients.files.files_client import get_files_client
from clients.files.files_schema import CreateFileRequestSchema
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from clients.exercises.exercises_client import get_exercises_client
from clients.exercises.exercises_schema import CreateExerciseRequestSchema

print("--- start api_client_create_exercise ---")

"""
Функция выполняет создание нового пользователя с уникальным email и заданным паролем.
:param: используется CreateUserRequestSchema с автоматической генерацией параметров.
:return: выводит в консоль данные созданного пользователя.
"""
public_users_client = get_public_users_client()

# Больше нет необходимости передавать значения, они будут генерироваться автоматически
create_user_request = CreateUserRequestSchema()
create_user_response = public_users_client.create_user(create_user_request)
print('Create user data:', create_user_response)

"""
Функция инициализирует объект AuthenticationUserSchema для аутентификации.
:param: email и password пользователя из сгенерированного запроса.
:return: AuthenticationUserSchema с этими данными.
"""
authentication_user = AuthenticationUserSchema(
    email=create_user_request.email,
    password=create_user_request.password
)

"""
Функция инициализирует API клиенты для работы с файлами, курсами и упражнениями.
:param: authentication_user — объект с учетными данными.
:return: объекты clients — files_client, courses_client, exercises_client.
"""
files_client = get_files_client(authentication_user)
courses_client = get_courses_client(authentication_user)
exercises_client = get_exercises_client(authentication_user)

"""
Функция загружает файл на сервер.
:param: CreateFileRequestSchema с автоматической генерацией параметров, кроме обязательных.
:return: выводит данные загруженного файла.
"""
create_file_request = CreateFileRequestSchema(
    upload_file="./testdata/files/image.png"
)
create_file_response = files_client.create_file(create_file_request)
print('Create file data:', create_file_response)

"""
Функция создает новый курс.
:param: CreateCourseRequestSchema с автоматической генерацией параметров, кроме обязательных.
:return: выводит данные созданного курса.
"""
create_course_request = CreateCourseRequestSchema(
    preview_file_id=create_file_response.file.id,
    created_by_user_id=create_user_response.user.id
)
create_course_response = courses_client.create_course(create_course_request)
print('Create course data:', create_course_response)

"""
Функция создает новое упражнение для курса.
:param: CreateExerciseRequestSchema с автоматической генерацией параметров, кроме обязательных.
:return: выводит данные созданного упражнения.
"""
create_exercise_request = CreateExerciseRequestSchema(
    course_id=create_course_response.course.id
)
create_exercise_response = exercises_client.create_exercise(create_exercise_request)
print('Create task data:', create_exercise_response)

print("--- end api_client_create_exercise ---")