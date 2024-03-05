from fastapi import FastAPI
from core.database import Base, engine as db_engine
from api.api_v1 import main
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings


app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main.router)


Base.metadata.create_all(db_engine)
