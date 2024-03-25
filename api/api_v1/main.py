from fastapi import APIRouter
from . import (routers_user, routers_login, routers_authority, routers_commission, routers_connector, routers_service,
               routers_address, routers_equipment)

router = APIRouter()

router.include_router(routers_user.router, prefix="/users", tags=["users"])
router.include_router(routers_login.router, prefix="/login", tags=["login"])
router.include_router(routers_authority.router, prefix="/authority", tags=["authority"])
router.include_router(routers_commission.router, prefix="/commission", tags=["commission"])
router.include_router(routers_connector.router, prefix="/connector", tags=["connector"])
router.include_router(routers_service.router, prefix="/service", tags=["service"])
router.include_router(routers_address.router, prefix="/address", tags=["address"])
router.include_router(routers_equipment.router, prefix="/equipment", tags=["equipment"])
