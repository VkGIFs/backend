# pylint: disable=unused-argument
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI, Request
from loguru import logger
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from starlette.responses import JSONResponse

from src.db import setup_db_connection
from src.exceptions import ApiException, InternalServerError
from src.settings import get_settings
from src.utils import bind_routes


settings = get_settings()

setup_db_connection(settings=settings)

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=1.0,
    enable_tracing=True,
    integrations=[
        StarletteIntegration(transaction_style="endpoint"),
        FastApiIntegration(transaction_style="endpoint"),
    ],
)


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):  # type: ignore
    """Lifespan context manager for managing application state"""

    yield


app = FastAPI(lifespan=lifespan)
bind_routes(app, get_settings())


@app.exception_handler(Exception)
async def common_exception_handler(_request: Request, exception: Exception):
    """Handler for all errors that breaks backend"""

    if settings.APP_MODE != "DEBUG":
        sentry_sdk.capture_exception(exception)
    error = InternalServerError(debug=str(exception))
    logger.error(f"***Pizdec*** Status code {error.status_code} Message: {error.message}")
    return JSONResponse(status_code=error.status_code, content=error.to_json())


@app.exception_handler(ApiException)
async def unicorn_api_exception_handler(_request: Request, exc: ApiException):
    """Handler for all errors that acknowledge"""

    sentry_sdk.capture_exception(exc)
    logger.error(f"***Zaebis*** Status code {exc.status_code} Message: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message},
    )
