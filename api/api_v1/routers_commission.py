from fastapi import APIRouter, HTTPException, status
from typing import List

from api.deps import SessionDep, CurrentUser
from crud.crud_commission import (crud_payment_type, crud_commission_value_type, crud_commission_type,
                                  crud_commission_group)

from schemas.schemas_commission import (PaymentTypeBase, CommissionValueTypeBase, CommissionTypeBase,
                                        CommissionTypeCreate, CommissionGroupBase)

router = APIRouter()


# Payment related endpoints
@router.post("/new-payment-type")
def create_payment_type(request: PaymentTypeBase, db: SessionDep):
    return crud_payment_type.create(db, obj_in=request)


@router.get("/all-payment_types", response_model=List[PaymentTypeBase])
async def get_all_payment_types(db: SessionDep):
    return crud_payment_type.get_all(db)


@router.put("/update-payment_type/{pk}")
async def update_payment_type(pk, request: PaymentTypeBase, db: SessionDep):
    db_obj = crud_payment_type.get_model_by_attribute(db, "cd", pk)
    return crud_payment_type.update(db, db_obj=db_obj, obj_in=request)


# Commission value type related endpoints
@router.post("/new-commission-value-type")
def create_commission_value_type(request: CommissionValueTypeBase, db: SessionDep):
    return crud_commission_value_type.create(db, obj_in=request)


@router.get("/all-commission_value_types", response_model=List[CommissionValueTypeBase])
async def get_all_commission_value_types(db: SessionDep):
    return crud_commission_value_type.get_all(db)


@router.put("/update-commission_value_type/{pk}")
async def update_commission_value_type(pk, request: CommissionValueTypeBase, db: SessionDep):
    db_obj = crud_commission_value_type.get_model_by_attribute(db, "cd", pk)
    return crud_commission_value_type.update(db, db_obj=db_obj, obj_in=request)


# Commission value type related endpoints
@router.post("/new-commission-type")
def create_commission_type(request: CommissionTypeCreate, db: SessionDep):
    return crud_commission_type.create(db, obj_in=request)


@router.get("/all-commission_types", response_model=List[CommissionTypeBase])
async def get_all_commission_types(db: SessionDep):
    return crud_commission_type.get_all(db)


@router.put("/update-commission_type/{pk}")
async def update_commission_type(pk, request: CommissionTypeCreate, db: SessionDep):
    db_obj = crud_commission_type.get_model_by_attribute(db, "cd", pk)
    return crud_commission_type.update(db, db_obj=db_obj, obj_in=request)


# Commission group related endpoints
@router.post("/new-commission-group")
def create_commission_group(request: CommissionGroupBase, db: SessionDep):
    return crud_commission_group.create(db, obj_in=request)


@router.get("/all-commission_groups", response_model=List[CommissionGroupBase])
async def get_all_commission_groups(db: SessionDep):
    return crud_commission_group.get_all(db)


@router.put("/update-commission_group/{pk}")
async def update_commission_group(pk, request: CommissionGroupBase, db: SessionDep):
    db_obj = crud_commission_group.get_model_by_attribute(db, "cd", pk)
    return crud_commission_group.update(db, db_obj=db_obj, obj_in=request)
