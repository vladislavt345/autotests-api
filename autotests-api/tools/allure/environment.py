import platform
import sys
from config import settings


def create_allure_environment_file():
    # Получаем информацию об операционной системе
    os_info = f"{platform.system()}, {platform.release()}"
    
    # Получаем информацию о версии Python
    python_version = sys.version
    
    # Создаем словарь с информацией об окружении
    environment_data = {
        'os_info': os_info,
        'python_version': python_version
    }
    
    # Создаем список из элементов в формате {key}={value}
    items = [f'{key}={value}' for key, value in environment_data.items()]
    
    # Собираем все элементы в единую строку с переносами
    properties = '\n'.join(items)

    # Открываем файл ./allure-results/environment.properties на запись
    with open(settings.allure_results_dir.joinpath('environment.properties'), 'w+') as file:
        file.write(properties)  # Записываем переменные в файл