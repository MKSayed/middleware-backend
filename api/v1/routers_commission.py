from fastapi import APIRouter, HTTPException, status
from typing import List

from api.deps import AsyncSessionDep, CurrentUserDep

from schemas.schemas_commission import (
    PaymentTypeBase,
    CommissionValueTypeBase,
    CommissionTypeBase,
    CommissionTypeCreate,
    CommissionGroupBase,
)

from models.models_commission import CommissionType, CommissionValueType, CommissionGroup, PaymentType

router = APIRouter()


# Payment related endpoints
@router.post("/payment-types")
async def create_payment_type(request: PaymentTypeBase, db: AsyncSessionDep):
    return await PaymentType(**request.model_dump(exclude_unset=True, exclude_none=True)).save(db)


@router.get("/payment-types", response_model=List[PaymentTypeBase])
async def get_all_payment_types(db: AsyncSessionDep):
    return await PaymentType.get_all(db)


@router.put("/payment-types/{pk}")
async def update_payment_type(pk, request: PaymentTypeBase, db: AsyncSessionDep):
    payment_type = await PaymentType.find(db, cd=pk)
    return await payment_type.update(db, **request.model_dump(exclude_unset=True, exclude_none=True))


# Commission value type related endpoints
@router.post("/commission-value-types")
async def create_commission_value_type(request: CommissionValueTypeBase, db: AsyncSessionDep):
    return await CommissionValueType(**request.model_dump(exclude_unset=True, exclude_none=True)).save(db)


@router.get("/commission-value-types", response_model=List[CommissionValueTypeBase])
async def get_all_commission_value_types(db: AsyncSessionDep):
    return await CommissionValueType.get_all(db)


@router.put("/commission-value-types/{pk}")
async def update_commission_value_type(
    pk, request: CommissionValueTypeBase, db: AsyncSessionDep
):
    commission_value_type = await CommissionValueType.find(db, cd=pk)
    return await commission_value_type.update(db, **request.model_dump(exclude_unset=True, exclude_none=True))


# Commission type related endpoints
@router.post("/commission-types")
async def create_commission_type(request: CommissionTypeCreate, db: AsyncSessionDep):
    return await CommissionType(**request.model_dump(exclude_unset=True, exclude_none=True)).save(db)


@router.get("/commission-types", response_model=List[CommissionTypeBase])
async def get_all_commission_types(db: AsyncSessionDep):
    return await CommissionType.get_all(db)


@router.put("/commission-types/{pk}")
async def update_commission_type(pk, request: CommissionTypeCreate, db: AsyncSessionDep):
    commission_type = await CommissionType.find(db, cd=pk)
    return await commission_type.update(db, **request.model_dump(exclude_unset=True, exclude_none=True))


# Commission group related endpoints
@router.post("/commission-groups")
async def create_commission_group(request: CommissionGroupBase, db: AsyncSessionDep):
    return await CommissionGroup(**request.model_dump(exclude_unset=True, exclude_none=True)).save(db)


@router.get("/commission-groups", response_model=List[CommissionGroupBase])
async def get_all_commission_groups(db: AsyncSessionDep):
    return await CommissionGroup.get_all(db)


@router.put("/commission-groups/{pk}")
async def update_commission_group(pk, request: CommissionGroupBase, db: AsyncSessionDep):
    commission_group = await CommissionGroup.find(db, cd=pk)
    return await commission_group.update(db, **request.model_dump(exclude_unset=True, exclude_none=True))
