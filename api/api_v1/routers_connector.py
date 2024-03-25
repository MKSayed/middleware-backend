from typing import List

from fastapi import APIRouter

from api.deps import SessionDep
from crud.crud_connector import crud_connector, crud_module

from schemas.schemas_connector import (ConnectorBase, ModuleBase)

router = APIRouter()


# Connector related endpoints
@router.post("/new-connector")
def create_connector(request: ConnectorBase, db: SessionDep):
    return crud_connector.create(db, obj_in=request)


@router.get("/all-connectors", response_model=List[ConnectorBase])
async def get_all_connectors(db: SessionDep):
    return crud_connector.get_all(db)


@router.put("/update-connector/{pk}")
async def update_connector(pk, request: ConnectorBase, db: SessionDep):
    db_obj = crud_connector.get_model_by_attribute(db, "id", pk)
    return crud_connector.update(db, db_obj=db_obj, obj_in=request)


# Module value type related endpoints
@router.post("/new-module")
def create_module(request: ModuleBase, db: SessionDep):
    return crud_module.create(db, obj_in=request)


@router.get("/all-modules", response_model=List[ModuleBase])
async def get_all_modules(db: SessionDep):
    return crud_module.get_all(db)


@router.put("/update-module/{pk}")
async def update_module(pk, request: ModuleBase, db: SessionDep):
    db_obj = crud_module.get_model_by_attribute(db, "cd", pk)
    return crud_module.update(db, db_obj=db_obj, obj_in=request)
