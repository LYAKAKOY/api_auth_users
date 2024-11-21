import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.auth.views import auth_user_router
from .external.postgres.connection import create_tables


app = FastAPI(
    title="API Auth JWT",
    version=os.getenv("APP_VERSION", default="DEV"),
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)


def create_app() -> FastAPI:
    app.include_router(auth_user_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", create_tables)
    return app
