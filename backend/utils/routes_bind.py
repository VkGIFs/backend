from fastapi import FastAPI

from backend.routes import list_of_routes
from backend.settings import Settings


def bind_routes(application: FastAPI, settings: Settings) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route, prefix=settings.PATH_PREFIX)
