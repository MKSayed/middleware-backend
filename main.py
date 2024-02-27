from fastapi import FastAPI
from models import models_authority
import database
from api.api_v1 import api
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

app.include_router(api.router)


database.Base.metadata.create_all(database.engine)
