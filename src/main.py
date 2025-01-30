from typing import Any

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from src.config import settings, AppSettings
from src.config.event import lifespan
from src.routes import router


class App:
    def __init__(self, event_manager: Any, router: APIRouter, settings: AppSettings):
        self.__app = FastAPI(lifespan=event_manager, **settings.set_app_attributes)  # noqa
        self.__setup_middlewares(settings=settings)
        self.__add_routes(router=router, settings=settings)
        self.__setup_scheduler()

    def __setup_middlewares(self, settings: AppSettings):
        self.__app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.ALLOWED_ORIGIN_LIST,
            allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
            allow_methods=settings.ALLOWED_METHODS,
            allow_headers=settings.ALLOWED_HEADER_LIST,
        )

    def __add_routes(self, router: APIRouter, settings: AppSettings):
        self.__app.include_router(router=router, prefix=settings.API_PREFIX)

    def __setup_scheduler(self):
        pass

    def __call__(self) -> FastAPI:
        return self.__app


def initialize_application() -> FastAPI:
    return App(event_manager=lifespan, router=router, settings=settings)()


app = initialize_application()

if __name__ == "__main__":
    run(
        app='main:app',
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.IS_DEBUG,
        workers=settings.WORKERS,
    )
