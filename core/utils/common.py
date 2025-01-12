from bcrypt import checkpw
from bcrypt import gensalt
from bcrypt import hashpw


def make_hashed_pwd(password: str) -> str:
    """
    Метод для хеширования пароля
    :param password: Исходный пароль
    :return: Хешированный пароль
    """
    return hashpw(password.encode('utf-8'), gensalt()).decode(encoding='utf-8')


def is_the_same_passwords(password: str, hashed: str) -> bool:
    """
    Проверка пароля.
    :param password: Исходный пароль
    :param hashed: Хешированный пароль
    :return: Верно ли указан пароль
    """
    return checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
