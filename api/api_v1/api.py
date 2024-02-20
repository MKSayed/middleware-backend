from fastapi import APIRouter
from api.api_v1.endpoints import routers_user

router = APIRouter()

router.include_router(routers_user.router, prefix="/users", tags=["users"])
