from clients.courses.courses_client import get_courses_client
from clients.courses.courses_schema import CreateCourseRequestSchema
from clients.files.files_client import get_files_client
from clients.files.files_schema import CreateFileRequestSchema
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from clients.exercises.exercises_client import get_exercises_client
from clients.exercises.exercises_schema import CreateExerciseRequestSchema
from tools.fakers import get_random_email

print("--- start api_client_create_exercise ---")

"""
Функция выполняет создание нового пользователя с уникальным email и заданным паролем.
:param: используется CreateUserRequestSchema с параметрами email, password, lastName, firstName, middleName.
:return: выводит в консоль данные созданного пользователя.
"""
public_users_client = get_public_users_client()
user_email = get_random_email()
user_password = "string"

create_user_request = CreateUserRequestSchema(
    email=user_email,
    password=user_password,
    last_name="string",
    first_name="string",
    middle_name="string"
)

create_user_response = public_users_client.create_user(create_user_request)
print('Create user data:', create_user_response)

"""
Функция инициализирует объект AuthenticationUserSchema для аутентификации.
:param: email и password пользователя.
:return: AuthenticationUserSchema с этими данными.
"""
authentication_user = AuthenticationUserSchema(
    email=user_email,
    password=user_password
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
:param: CreateFileRequestSchema с параметрами filename, directory, upload_file.
:return: выводит данные загруженного файла.
"""
create_file_request = CreateFileRequestSchema(
    filename="image.png",
    directory="courses",
    upload_file="./testdata/files/image.png"
)

create_file_response = files_client.create_file(create_file_request)
print('Create file data:', create_file_response)

"""
Функция создает новый курс.
:param: CreateCourseRequestSchema с параметрами title, max_score, min_score, description, estimated_time, preview_file_id, created_by_user_id.
:return: выводит данные созданного курса.
"""
create_course_request = CreateCourseRequestSchema(
    title="Python Course",
    max_score=100,
    min_score=10,
    description="Python API course.",
    estimated_time="4 weeks",
    preview_file_id=create_file_response.file.id,
    created_by_user_id=create_user_response.user.id
)

create_course_response = courses_client.create_course(create_course_request)
print('Create course data:', create_course_response)

"""
Функция создает новое упражнение для курса.
:param: CreateExerciseRequestSchema с параметрами title, course_id, max_score, min_score, order_index, description, estimated_time.
:return: выводит данные созданного упражнения.
"""
create_exercise_request = CreateExerciseRequestSchema(
    title="First Exercise",
    course_id=create_course_response.course.id,
    max_score=20,
    min_score=5,
    order_index=1,
    description="This is the first exercise for the Python course.",
    estimated_time="1 hour"
)

create_exercise_response = exercises_client.create_exercise(create_exercise_request)
print('Create task data:', create_exercise_response)

print("--- end api_client_create_exercise ---")