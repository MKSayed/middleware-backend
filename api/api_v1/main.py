from fastapi import APIRouter
from . import routers_user, routers_login, routers_authority

router = APIRouter()

router.include_router(routers_user.router, prefix="/users", tags=["users"])
router.include_router(routers_login.router, prefix="/login", tags=["login"])
router.include_router(routers_authority.router, prefix="/authority", tags=["authority"])
