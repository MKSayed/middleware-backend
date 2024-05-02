from typing import Optional, Union

from fastapi import APIRouter, Query
from pydantic import parse_obj_as

from api.deps import SessionDep
from crud.crud_service import (crud_service_parameter, crud_currency, crud_service_parameter_type, crud_provider,
                               crud_service_group, crud_service, crud_service_price, crud_service_charge)
from schemas.schemas_service import (ServiceBase, ServiceParameterTypeBase, ServiceGroupBase, ServicePriceBase,
                                     CurrencyBase, ProviderBase, ServiceChargeBase, ServiceParameterBase,
                                     ServiceDisplayShort, CurrencyDisplayShort)

router = APIRouter()


# Currency related endpoints
@router.post("/new-currency")
def create_currency(request: CurrencyBase, db: SessionDep):
    return crud_currency.create(db, obj_in=request)


@router.get("/all-currencies", response_model=list[Union[CurrencyBase, CurrencyDisplayShort]])
async def get_all_currencies(
        db: SessionDep,
        short: bool | None = Query(False, description="Whether to return the short version of the data")
):
    currencies = crud_currency.get_all(db)
    if short:
        return parse_obj_as(list[CurrencyDisplayShort], currencies)
    return currencies


@router.put("/update-currency/{pk}")
async def update_currency(pk, request: CurrencyBase, db: SessionDep):
    db_obj = crud_currency.get_model_by_attribute(db, "id", pk)
    return crud_currency.update(db, db_obj=db_obj, obj_in=request)


# Provider related endpoints
@router.post("/new-provider")
def create_provider(request: ProviderBase, db: SessionDep):
    return crud_provider.create(db, obj_in=request)


@router.get("/all-providers", response_model=list[ProviderBase])
async def get_all_providers(db: SessionDep):
    return crud_provider.get_all(db)


@router.put("/update-provider/{pk}")
async def update_commission_value_type(pk, request: ProviderBase, db: SessionDep):
    db_obj = crud_provider.get_model_by_attribute(db, "id", pk)
    return crud_provider.update(db, db_obj=db_obj, obj_in=request)


# Service parameter type related endpoints
@router.post("/new-service-parameter-type")
def create_service_parameter_type(request: ServiceParameterTypeBase, db: SessionDep):
    return crud_service_parameter_type.create(db, obj_in=request)


@router.get("/all-service-parameter-types", response_model=list[ServiceParameterTypeBase])
async def get_all_service_parameter_types(db: SessionDep):
    return crud_service_parameter_type.get_all(db)


@router.put("/update-service-parameter-type/{pk}")
async def update_service_parameter_type(pk, request: ServiceParameterTypeBase, db: SessionDep):
    db_obj = crud_service_parameter_type.get_model_by_attribute(db, "cd", pk)
    return crud_service_parameter_type.update(db, db_obj=db_obj, obj_in=request)


# Service group related endpoints
@router.post("/new-service-group")
def create_service_group(request: ServiceGroupBase, db: SessionDep):
    return crud_service_group.create(db, obj_in=request)


@router.get("/all-service-groups", response_model=list[ServiceGroupBase])
async def get_all_service_groups(db: SessionDep):
    return crud_service_group.get_all(db)


@router.put("/update-service-group/{pk}")
async def update_service_group(pk, request: ServiceGroupBase, db: SessionDep):
    db_obj = crud_service_group.get_model_by_attribute(db, "no", pk)
    return crud_service_group.update(db, db_obj=db_obj, obj_in=request)


# Service charge related endpoints
@router.post("/new-service-charge")
def create_service_charge(request: ServiceChargeBase, db: SessionDep):
    return crud_service_charge.create(db, obj_in=request)


@router.get("/all-service-charges", response_model=list[ServiceChargeBase])
async def get_all_service_charges(db: SessionDep):
    return crud_service_charge.get_all(db)


@router.put("/update-service-charge/{pk}")
async def update_service_charge(pk, request: ServiceChargeBase, db: SessionDep):
    db_obj = crud_service_charge.get_model_by_attribute(db, "cd", pk)
    return crud_service_charge.update(db, db_obj=db_obj, obj_in=request)


# Service related endpoints
@router.post("/new-service")
def create_service(request: ServiceBase, db: SessionDep):
    return crud_service.create(db, obj_in=request)


@router.get("/all-services", response_model=list[Union[ServiceBase, ServiceDisplayShort]])
async def get_all_services(
        db: SessionDep,
        short: bool | None = Query(False, description="Whether to return the short version of the data")):
    services = crud_service.get_all(db)
    if short:
        return parse_obj_as(list[ServiceDisplayShort], services)
    return services


@router.put("/update-service/{pk}")
async def update_service(pk, request: ServiceBase, db: SessionDep):
    db_obj = crud_service.get_model_by_attribute(db, "id", pk)
    return crud_service.update(db, db_obj=db_obj, obj_in=request)


# Service price related endpoints
@router.post("/new-service-price")
def create_service_price(request: ServicePriceBase, db: SessionDep):
    return crud_service_price.create(db, obj_in=request)


@router.get("/all-service-prices", response_model=list[ServicePriceBase])
async def get_all_service_prices(db: SessionDep):
    return crud_service_price.get_all(db)


@router.put("/update-service-price/{pk}")
async def update_service_price(pk, request: ServicePriceBase, db: SessionDep):
    db_obj = crud_service_price.get_model_by_attribute(db, "id", pk)
    return crud_service_price.update(db, db_obj=db_obj, obj_in=request)


# Service parameter related endpoints
@router.post("/new-service-parameter")
def create_service_parameter(request: ServiceParameterBase, db: SessionDep):
    return crud_service_parameter.create(db, obj_in=request)


@router.get("/all-service-parameters", response_model=list[ServiceParameterBase])
async def get_all_service_parameters(db: SessionDep):
    return crud_service_parameter.get_all(db)


@router.put("/update-service-parameter/{pk}")
async def update_service_parameter(pk, request: ServiceParameterBase, db: SessionDep):
    db_obj = crud_service_parameter.get_model_by_attribute(db, "ser", pk)
    return crud_service_parameter.update(db, db_obj=db_obj, obj_in=request)
