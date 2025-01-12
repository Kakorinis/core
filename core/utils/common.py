from typing import List
from typing import Type

from bcrypt import checkpw
from bcrypt import gensalt
from bcrypt import hashpw
from dependency_injector import containers
from fastapi import APIRouter
from fastapi import FastAPI


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


def create_app(depends_container: Type[containers.DeclarativeContainer], routers: List[APIRouter]) -> FastAPI:
    container = depends_container()

    # FastAPI и Starlette реализуют OPTIONS поддержку, но в запросах должны быть установлены оба заголовка Origin и Access-Control-Request-Method
    # https://github.com/fastapi/fastapi/issues/1849
    # from starlette.middleware import Middleware
    # from starlette.middleware.cors import CORSMiddleware
    # origins = ["http://newstyle.ru:8092"]
    # middleware = [
    #     Middleware(
    #         CORSMiddleware,
    #         allow_origins=["*"],  # origins если [*], то в чем смысл защиты?
    #         allow_credentials=True,
    #         allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    #         allow_headers=['X-CSRF-Token', 'X-Requested-With', 'Accept', 'Accept-Version', 'Content-Length',
    #                        'Content-MD5', 'Content-Type', 'Date', 'X-Api-Version', 'Authorization']
    #     )
    # ]

    # application = FastAPI(middleware=middleware)
    application = FastAPI()
    application.container = container
    for router in routers:
        application.include_router(router)
    return application
