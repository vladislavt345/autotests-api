from clients.courses.courses_client import get_courses_client, CreateCourseRequestDict
from clients.files.files_client import get_files_client, CreateFileRequestDict
from clients.private_http_builder import AuthenticationUserDict
from clients.users.public_users_client import get_public_users_client, CreateUserRequestDict
from clients.exercises.exercises_client import get_exercises_client, CreateExerciseRequestDict
from tools.fakers import get_random_email

print("--- start api_client_create_exercise ---")

"""
Функция выполняет создание нового пользователя с уникальным email и заданным паролем.

:param: используется CreateUserRequestDict с параметрами email, password, lastName, firstName, middleName.
:return: выводит в консоль данные созданного пользователя.
"""
public_users_client = get_public_users_client()
user_email = get_random_email()

user_password = "string"
create_user_request = CreateUserRequestDict(
    email=user_email,
    password=user_password,
    lastName="string",
    firstName="string",
    middleName="string"
)
create_user_response = public_users_client.create_user(create_user_request)
print('Create user data:', create_user_response)

"""
Функция инициализирует объект AuthenticationUserDict для аутентификации.

:param: email и password пользователя.
:return: AuthenticationUserDict с этими данными.
"""
authentication_user = AuthenticationUserDict(
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

:param: CreateFileRequestDict с параметрами filename, directory, upload_file.
:return: выводит данные загруженного файла.
"""
create_file_request = CreateFileRequestDict(
    filename="image.png",
    directory="courses",
    upload_file="./testdata/files/image.png"
)
create_file_response = files_client.create_file(create_file_request)
print('Create file data:', create_file_response)

"""
Функция создает новый курс.

:param: CreateCourseRequestDict с параметрами title, maxScore, minScore, description, estimatedTime, previewFileId, createdByUserId.
:return: выводит данные созданного курса.
"""
create_course_request = CreateCourseRequestDict(
    title="Python Course",
    maxScore=100,
    minScore=10,
    description="Python API course.",
    estimatedTime="4 weeks",
    previewFileId=create_file_response['file']['id'],
    createdByUserId=create_user_response['user']['id']
)
create_course_response = courses_client.create_course_api(create_course_request).json()
print('Create course data:', create_course_response)

"""
Функция создает новое упражнение для курса.

:param: CreateExerciseRequestDict с параметрами title, courseId, maxScore, minScore, orderIndex, description, estimatedTime.
:return: выводит данные созданного упражнения.
"""
create_exercise_request = CreateExerciseRequestDict(
    title="First Exercise",
    courseId=create_course_response['course']['id'],
    maxScore=20,
    minScore=5,
    orderIndex=1,
    description="This is the first exercise for the Python course.",
    estimatedTime="1 hour"
)
create_exercise_response = exercises_client.create_exercise(create_exercise_request)
print('Create task data:', create_exercise_response)
print("--- end api_client_create_exercise ---")