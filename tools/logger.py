import logging

def get_logger(name: str) -> logging.Logger:
    """
    Инициализирует и возвращает логгер с указанным именем.

    Настройки логгера:
    - Уровень логирования: DEBUG (обрабатывает все сообщения от DEBUG и выше)
    - Обработчик: StreamHandler для вывода в консоль
    - Формат сообщений: '<время> | <имя логгера> | <уровень> | <сообщение>'

    Args:
        name (str): Имя логгера.

    Returns:
        logging.Logger: Настроенный экземпляр логгера.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger