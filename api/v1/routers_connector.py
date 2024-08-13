import asyncio

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import TypeAdapter, BaseModel

from api.deps import AsyncSessionDep
from models.models_service import Service

from schemas.schemas_connector import (
    ConnectorBase,
    ModuleBase,
    ModuleParameterBase,
    ModuleCreate,
    ModuleParameterCreate,
    ConnectorDisplayShort, ConnectorDisplay, ModuleParameterCreateWithoutFK, ModuleParameterDisplayWithChildren,
)
from schemas.schemas_service import ServiceDisplay
from models.models_connector import Connector, Module, ModuleParameter

router = APIRouter()


# Connector related endpoints
@router.post("/connectors")
async def create_connector(request: ConnectorBase, db: AsyncSessionDep):
    return await Connector(
        **request.model_dump(exclude_unset=True, exclude_none=True)
    ).save(db)


@router.get("/connectors/{pk}", response_model=ConnectorBase)
async def get_connector(pk: int, db: AsyncSessionDep):
    return await Connector.find(db, id=pk)


@router.get(
    "/connectors", response_model=list[ConnectorDisplay | ConnectorDisplayShort]
)
async def get_all_connectors(
    db: AsyncSessionDep,
    short: bool | None = Query(
        False, description="Whether to return the short version of the data"
    ),
):
    await asyncio.sleep(3)
    if short:
        connectors = await Connector.get_all(db)
        short_connectors = TypeAdapter(list[ConnectorDisplayShort])
        return short_connectors.validate_python(connectors)
    else:
        return await Connector.get_all_with_service_count(db)


@router.put("/connectors/{pk}")
async def update_connector(pk: int, request: ConnectorBase, db: AsyncSessionDep):
    connector = await Connector.find(db, id=pk)
    return await connector.update(db, **request.model_dump(exclude_unset=True, exclude_none=True))


@router.get("/connectors/{pk}/modules", response_model=list[ModuleBase])
async def get_all_modules_for_connector(pk: int, db: AsyncSessionDep):
    return await Module.find_all(db, fk_connector_id=pk)


class ConnectorServices(BaseModel):
    services: list[ServiceDisplay]
    connector_name: str


@router.get("/connectors/{pk}/services", response_model=ConnectorServices)
async def get_all_services_for_connector(pk: int, db: AsyncSessionDep):
    module_ids = await Module.get_all_module_ids_for_connector(db, connector_id=pk)
    services = await Service.find_all(db, with_eager_loading=True, fk_module_id=module_ids)
    connector = await Connector.find(db, id=pk)
    connector_name = connector.name

    return ConnectorServices(services=services, connector_name=connector_name)


# Module related endpoints
@router.post("/modules")
async def create_module(request: ModuleCreate, db: AsyncSessionDep):
    module_in = ModuleBase.model_validate(request.model_dump())
    new_module = await Module(**module_in.model_dump(exclude_unset=True, exclude_none=True)).save(db)
    module_id = new_module.id
    try:
        for module_param in request.module_params:
            module_parameter_in = ModuleParameterCreate(
                **module_param.model_dump(), fk_module_id=module_id
            )
            module_parameter = await ModuleParameter(**module_parameter_in.model_dump(exclude_none=True, exclude_unset=True)).save(db, auto_commit=False)

        await db.commit()
    except Exception as e:
        await db.rollback()
        await db.delete(new_module)
        await db.commit()
        raise e

    return JSONResponse(
        {"message": "Module was created successfully"},
        status_code=status.HTTP_201_CREATED,
    )


@router.get("/modules", response_model=list[ModuleBase])
async def get_all_modules(db: AsyncSessionDep):
    return await Module.get_all(db)


@router.get("/modules/{pk}", response_model=ModuleBase)
async def get_module(pk: int, db: AsyncSessionDep):
    return await Module.find(db, id=pk)


@router.put("/modules/{pk}")
async def update_module(pk: int, request: ModuleBase, db: AsyncSessionDep):
    module = await Module.find(db, id=pk)
    return await module.update(db, **request.model_dump(exclude_unset=True, exclude_none=True))


@router.get("/modules/{pk}/parameters", response_model=list[ModuleParameterBase | ModuleParameterDisplayWithChildren])
async def get_all_params_for_module(pk: int, db: AsyncSessionDep, nested_form: bool = Query()):
    module_parameters = await ModuleParameter.find_all(db, with_eager_loading=True, fk_module_id=pk)

    if nested_form:
        root_parameters = []
        parameter_collection = {}
        for param in sorted(module_parameters, key=lambda x: int(x.nest_level)):
            if param.nest_level == 0:
                root_parameters.append(param)
                parameter_collection[param.id] = param
            else:
                if hasattr(parameter_collection[param.parent_id], "children"):
                    parameter_collection[param.parent_id].children.append(param)
                    parameter_collection[param.id] = param
                else:
                    parameter_collection[param.parent_id].children = [param]
                    parameter_collection[param.id] = param
        nest = TypeAdapter(list[ModuleParameterDisplayWithChildren])
        return nest.validate_python(root_parameters)

    return module_parameters


# Module Parameter related endpoints
@router.post("/module-parameters")
async def create_module_parameter(request: ModuleParameterCreate, db: AsyncSessionDep):

    return await ModuleParameter(**request.model_dump(exclude_unset=True, exclude_none=True)).save(db)


@router.put("/module-parameters/{pk}")
async def update_module_parameter(pk: int, request: ModuleParameterCreateWithoutFK, db: AsyncSessionDep):
    module_parameter = await ModuleParameter.find(db, id=pk)
    return await module_parameter.update(db, **request.model_dump(exclude_unset=True, exclude_none=True))
