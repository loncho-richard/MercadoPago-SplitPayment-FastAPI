from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api_v1 import router as api_v1_router
from app.api.deps import create_db_and_tables
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown logic here

app = FastAPI(
    title="Split Payments Marketplace",
    description="API para marketplace con split payments usando Mercado Pago",
    version="1.0.0",
    lifespan=lifespan,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    redoc_url=None if settings.ENVIRONMENT == "production" else "/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(api_v1_router, prefix="/api/v1")