from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api_v1 import router as api_v1_router
from app.api.deps import create_db_and_tables
from app.core.config import settings
from app.core.security import oauth2_scheme
from app.core.config import settings


app = FastAPI(
    swagger_ui_init_oauth={
        "clientId": "fastapi-client",
        "scopes": "read write"
    },
    security=[{"Bearer": []}]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(api_v1_router, prefix="/api")