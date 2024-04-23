from typing import List

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.orm import Session

from api.deps import SessionDep
from crud.crud_connector import crud_connector, crud_module, crud_module_parameter

from schemas.schemas_connector import ConnectorBase, ModuleBase, ModuleParameter, ModuleCreate, ModuleParameterCreate

router = APIRouter()


# Connector related endpoints
@router.post("/new-connector")
def create_connector(request: ConnectorBase, db: SessionDep):
    return crud_connector.create(db, obj_in=request)


@router.get("/get-connector/{pk}", response_model=ConnectorBase)
async def get_connector(pk: int, db: SessionDep):
    return crud_connector.get_model_by_attribute(db, "id", pk)


@router.get("/all-connectors", response_model=List[ConnectorBase])
async def get_all_connectors(db: SessionDep):
    return crud_connector.get_all(db)


@router.put("/update-connector/{pk}")
async def update_connector(pk, request: ConnectorBase, db: SessionDep):
    db_obj = crud_connector.get_model_by_attribute(db, "id", pk)
    return crud_connector.update(db, db_obj=db_obj, obj_in=request)


# Module related endpoints
@router.post("/new-module")
def create_module(request: ModuleCreate, db: SessionDep):
    module_in = ModuleBase.model_validate(request.model_dump())
    created_module = crud_module.create(db, obj_in=module_in)
    module_id = created_module.id
    for module_param in request.module_params:
        module_parameter_in = ModuleParameterCreate(**module_param.model_dump(), fk_moduleid=module_id)
        module_parameter = crud_module_parameter.create(db, obj_in=module_parameter_in)
    return JSONResponse({"message": "Module was created successfully"}, status_code=status.HTTP_201_CREATED)


@router.get("/get-module/{pk}", response_model=ModuleBase)
async def get_module(pk: int, db: SessionDep):
    return crud_module.get_model_by_attribute(db, "id", pk)


@router.get("/all-modules", response_model=List[ModuleBase])
async def get_all_modules(db: SessionDep):
    return crud_module.get_all(db)


@router.get("/all-modules-for-connector/{pk}", response_model=List[ModuleBase])
async def get_all_modules_for_connector(pk, db: SessionDep):
    return crud_module.get_models_by_attribute(db, "fk_connectorid", pk)


@router.put("/update-module/{pk}")
async def update_module(pk, request: ModuleBase, db: SessionDep):
    db_obj = crud_module.get_model_by_attribute(db, "id", pk)
    return crud_module.update(db, db_obj=db_obj, obj_in=request)


# Module Parameter related endpoints
@router.post("/new-module-parameter")
def create_module_parameter(request: ModuleParameter, db: SessionDep):
    return crud_module_parameter.create(db, obj_in=request)


@router.get("/all-params-for-module/{pk}", response_model=List[ModuleParameter])
async def get_all_params_for_module(pk, db: SessionDep):
    return crud_module_parameter.get_models_by_attribute(db, "fk_moduleid", pk)


@router.put("/update-module-parameter/{pk}")
async def update_module_parameter(pk, request: ModuleParameter, db: SessionDep):
    db_obj = crud_module_parameter.get_model_by_attribute(db, "id", pk)
    return crud_module_parameter.update(db, db_obj=db_obj, obj_in=request)
