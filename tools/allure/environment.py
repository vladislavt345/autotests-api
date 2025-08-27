import platform
import sys
from config import settings


def create_allure_environment_file():
    # Информация об операционной системе
    os_info = f"{platform.system()}, {platform.release()}"
    
    # Информация о версии Python
    python_version = sys.version
    
    # Словарь с информацией об окружении
    environment_data = {
        'os_info': os_info,
        'python_version': python_version
    }
    
    items = [f'{key}={value}' for key, value in environment_data.items()]
    properties = '\n'.join(items)

    with open(settings.allure_results_dir.joinpath('environment.properties'), 'w+') as file:
        file.write(properties)
