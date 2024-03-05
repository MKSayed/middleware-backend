from fastapi import APIRouter, HTTPException
from starlette import status

from api.deps import SessionDep, CurrentUser
from crud import crud_transaction_kiosk
from schemas.schemas_authority import PermissionCreate

router = APIRouter()
# current_user: CurrentUser

@router.get("")
async def get_all_transactions(db: SessionDep):
    return crud_transaction_kiosk.get_all(db)


@router.post("/new-transaction")
async def create_transaction(request: PermissionCreate, db: SessionDep):
    return crud_transaction_kiosk.create(db, obj_in=request)


@router.put("/update-transaction/{update_key}")
async def create_transaction(update_key, request: PermissionCreate, db: SessionDep):
    db_obj = crud_transaction_kiosk.get_model_by_attribute(db, "number", update_key)
    # raise HTTPException(sta   tus_code=status.HTTP_404_NOT_FOUND,)
    return crud_transaction_kiosk.update(db, db_obj=db_obj, obj_in=request)
