import asyncio
from typing import List, Union, Optional

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import TypeAdapter

from api.deps import SessionDep
from crud.crud_connector import crud_connector, crud_module, crud_module_parameter

from schemas.schemas_connector import (
    ConnectorBase,
    ModuleBase,
    ModuleParameter,
    ModuleCreate,
    ModuleParameterCreate,
    ConnectorDisplayShort, ConnectorDisplay,
)

router = APIRouter()


# Connector related endpoints
@router.post("/connectors")
def create_connector(request: ConnectorBase, db: SessionDep):
    return crud_connector.create(db, obj_in=request)


@router.get("/connectors/{pk}", response_model=ConnectorBase)
async def get_connector(pk: int, db: SessionDep):
    return crud_connector.get_model_by_attribute(db, "id", pk)


@router.get(
    "/connectors", response_model=list[Union[ConnectorDisplay, ConnectorDisplayShort]]
)
async def get_all_connectors(
    db: SessionDep,
    short: bool | None = Query(
        False, description="Whether to return the short version of the data"
    ),
):
    await asyncio.sleep(3)
    if short:
        connectors = crud_connector.get_all(db)
        short_connectors = TypeAdapter(list[ConnectorDisplayShort])
        return short_connectors.validate_python(connectors)
    else:
        return crud_connector.get_all_with_service_count(db)



@router.put("/connectors/{pk}")
async def update_connector(pk: int, request: ConnectorBase, db: SessionDep):
    db_obj = crud_connector.get_model_by_attribute(db, "id", pk)
    return crud_connector.update(db, db_obj=db_obj, obj_in=request)


@router.get("/connectors/{pk}/modules", response_model=List[ModuleBase])
async def get_all_modules_for_connector(pk: int, db: SessionDep):
    return crud_module.get_models_by_attribute(db, "fk_connectorid", pk)


# Module related endpoints
@router.post("/modules")
def create_module(request: ModuleCreate, db: SessionDep):
    module_in = ModuleBase.model_validate(request.model_dump())
    created_module = crud_module.create(db, obj_in=module_in)
    module_id = created_module.id
    for module_param in request.module_params:
        module_parameter_in = ModuleParameterCreate(
            **module_param.model_dump(), fk_moduleid=module_id
        )
        module_parameter = crud_module_parameter.create(db, obj_in=module_parameter_in)
    return JSONResponse(
        {"message": "Module was created successfully"},
        status_code=status.HTTP_201_CREATED,
    )


@router.get("/modules", response_model=List[ModuleBase])
async def get_all_modules(db: SessionDep):
    return crud_module.get_all(db)


@router.get("/modules/{pk}", response_model=ModuleBase)
async def get_module(pk: int, db: SessionDep):
    return crud_module.get_model_by_attribute(db, "id", pk)


@router.put("/modules/{pk}")
async def update_module(pk: int, request: ModuleBase, db: SessionDep):
    db_obj = crud_module.get_model_by_attribute(db, "id", pk)
    return crud_module.update(db, db_obj=db_obj, obj_in=request)


@router.get("/modules/{pk}/parameters", response_model=List[ModuleParameter])
async def get_all_params_for_module(pk: int, db: SessionDep):
    return crud_module_parameter.get_models_by_attribute(db, "fk_moduleid", pk)


# Module Parameter related endpoints
@router.post("/module-parameters")
def create_module_parameter(request: ModuleParameter, db: SessionDep):
    return crud_module_parameter.create(db, obj_in=request)


@router.put("/module-parameters/{pk}")
async def update_module_parameter(pk: int, request: ModuleParameter, db: SessionDep):
    db_obj = crud_module_parameter.get_model_by_attribute(db, "id", pk)
    return crud_module_parameter.update(db, db_obj=db_obj, obj_in=request)
