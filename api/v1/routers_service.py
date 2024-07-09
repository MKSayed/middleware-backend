from typing import Union, Annotated
from colorama import Fore, Style

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

from pydantic import parse_obj_as, TypeAdapter

from api.deps import AsyncSessionDep
from crud.crud_service import (
    crud_service_parameter,
    crud_currency,
    crud_service_parameter_type,
    crud_provider,
    crud_service_group,
    crud_service,
    crud_service_price,
    crud_service_charge,
    crud_service_service_group_association,
)

from schemas.schemas_service import (
    ServiceBase,
    ServiceParameterTypeBase,
    ServiceGroupBase,
    ServicePriceBase,
    CurrencyBase,
    ProviderBase,
    ServiceChargeBase,
    ServiceParameterBase,
    ServiceDisplayShort,
    CurrencyDisplayShort,
    ServiceDisplay,
    ServiceCreate,
)
from models.models_service import (
    Currency,
    Provider,
    ServiceParameter,
    ServiceCharge,
    ServiceParameterType,
    ServiceServiceGroupAssociation,
    Service,
    ServiceGroup,
    ServicePrice,
)

router = APIRouter()


# Currencies related endpoints
@router.post("/currencies")
async def create_currency(request: CurrencyBase, db: AsyncSessionDep):
    return await Currency(
        **request.model_dump(exclude_unset=True, exclude_none=True)
    ).save(db)


@router.get(
    "/currencies", response_model=list[Union[CurrencyBase, CurrencyDisplayShort]]
)
async def get_all_currencies(
    db: AsyncSessionDep,
    short: bool | None = Query(
        False, description="Whether to return the short version of the data"
    ),
):
    currencies = await Currency.get_all(db)
    if short:
        currency_short_adapter = TypeAdapter(list[CurrencyDisplayShort])
        return currency_short_adapter.validate_python(currencies)
    return currencies


@router.put("/currencies/{pk}")
async def update_currency(pk, request: CurrencyBase, db: AsyncSessionDep):
    currency = await Currency.find(db, id=pk)
    return await currency.update(db, **request.model_dump(exclude_unset=True, exclude_none=True))


# Providers related endpoints
@router.post("/providers")
async def create_provider(request: ProviderBase, db: AsyncSessionDep):
    return await Provider(**request.model_dump(exclude_unset=True, exclude_none=True)).save(db)


@router.get("/providers", response_model=list[ProviderBase])
async def get_all_providers(db: AsyncSessionDep):
    return await Provider.get_all(db)


@router.put("/providers/{pk}")
async def update_provider(pk: int, request: ProviderBase, db: AsyncSessionDep):
    provider = await Provider.find(db, id=pk)
    return await provider.update(db, **request.model_dump(exclude_unset=True, exclude_none=True))


@router.get("/providers/{pk}/services")
async def get_provider_services(pk: int, db: AsyncSessionDep):
    return await Service.find(db, fk_providerid=pk)


# Service parameter type related endpoints
@router.post("/service-parameter-types")
async def create_service_parameter_type(request: ServiceParameterTypeBase, db: AsyncSessionDep):
    return await ServiceParameterType(**request.model_dump(exclude_unset=True, exclude_none=True)).save(db)


@router.get("/service-parameter-types", response_model=list[ServiceParameterTypeBase])
async def get_all_service_parameter_types(db: AsyncSessionDep):
    return await ServiceParameterType.get_all(db)


@router.put("/service-parameter-type/{pk}")
async def update_service_parameter_type(
    pk, request: ServiceParameterTypeBase, db: AsyncSessionDep
):
    service_parameter_type = await ServiceParameterType.find(db, cd=pk)
    return await service_parameter_type.update(db, **request.model_dump(exclude_unset=True, exclude_none=True))


# Service group related endpoints
@router.post("/service-groups")
async def create_service_group(request: ServiceGroupBase, db: AsyncSessionDep):
    return await ServiceGroup(**request.model_dump(exclude_unset=True, exclude_none=True)).save(db)


@router.get("/service-groups", response_model=list[ServiceGroupBase])
async def get_all_service_groups(db: AsyncSessionDep):
    return await ServiceGroup.get_all(db)


@router.put("/service-groups/{pk}")
async def update_service_group(pk, request: ServiceGroupBase, db: AsyncSessionDep):
    service_group = await ServiceGroup.find(db, no=pk)
    return await service_group.update(db, **request.model_dump(exclude_unset=True, exclude_none=True))


# Service charge related endpoints
@router.post("/service-charges")
async def create_service_charge(request: ServiceChargeBase, db: AsyncSessionDep):
    return await ServiceCharge(**request.model_dump(exclude_unset=True)).save(db)


@router.get("/service-charges", response_model=list[ServiceChargeBase])
async def get_all_service_charges(db: AsyncSessionDep):
    return await ServiceCharge.get_all(db)


@router.put("/service-charges/{pk}")
async def update_service_charge(pk, request: ServiceChargeBase, db: AsyncSessionDep):
    service_charge = await ServiceCharge.find(db, cd=pk)
    return await service_charge.update(db, **request.model_dump(exclude_unset=True))


# Service related endpoints
@router.post("/services")
async def create_service(request: ServiceCreate, db: AsyncSessionDep):
    service = await Service(**request.model_dump(include={"ar_name", "eng_name", "fk_moduleid", "fk_providerid"})).save(db, auto_commit=True)
    service_price_request_dict = request.model_dump(exclude={"ar_name", "eng_name", "fk_moduleid", "fk_providerid"})
    service_price_request_dict["fk_serviceid"] = service.id

    # rename price_type to type
    service_price_request_dict["type"] = service_price_request_dict.pop("price_type")

    try:
        service_price = await ServicePrice(**service_price_request_dict).save(db)
    except Exception as e:
        print(Fore.RED + str(e.with_traceback(None)) + Style.RESET_ALL)
        db.rollback()
        db.delete(service)
        db.commit()
        return JSONResponse(
            {"message": "An error occurred while creating service"},
            status_code=status.HTTP_417_EXPECTATION_FAILED,
        )
    return JSONResponse(
        {"message": "Service was created successfully"},
        status_code=status.HTTP_201_CREATED,
    )


@router.get("/services", response_model=list[ServiceDisplay | ServiceDisplayShort])
async def get_all_services(
    db: AsyncSessionDep,
    short: bool | None = Query(
        False, description="Whether to return the short version of the data"
    ),
):
    services = await Service.get_all(db)
    if short:
        short_services_adapter = TypeAdapter(list[ServiceDisplayShort])
        return short_services_adapter.validate_python(services)
    return services


@router.put("/services/{pk}")
async def update_service(pk, request: ServiceBase, db: AsyncSessionDep):
    service = await Service.find(db, id=pk)
    return await service.update(db, **request.model_dump(exclude_unset=True))


# Service price related endpoints
@router.post("/service-prices")
async def create_service_price(request: ServicePriceBase, db: AsyncSessionDep):
    return await ServicePrice(**request.model_dump(exclude_unset=True, exclude_none=True)).save(db)


@router.get("/service-prices", response_model=list[ServicePriceBase])
async def get_all_service_prices(db: AsyncSessionDep):
    return await ServicePrice.get_all(db)


@router.put("/service-prices/{pk}")
async def update_service_price(pk, request: ServicePriceBase, db: AsyncSessionDep):
    service_price = await ServicePrice.find(db, id=pk)
    return await service_price.update(db, **request.model_dump(exclude_none=True, exclude_unset=True))


# Service parameter related endpoints
@router.post("/service-parameters")
async def create_service_parameter(request: ServiceParameterBase, db: AsyncSessionDep):
    return await ServiceParameter(**request.model_dump(exclude_unset=True, exclude_none=True)).save(db)


@router.get("/service-parameters", response_model=list[ServiceParameterBase])
async def get_all_service_parameters(db: AsyncSessionDep):
    return await ServiceParameter.get_all(db)


@router.put("/service-parameters/{pk}")
async def update_service_parameter(pk, request: ServiceParameterBase, db: AsyncSessionDep):
    service_parameter = await ServiceParameter.find(db, ser=pk)
    return await service_parameter.update(db, **request.model_dump(exclude_unset=True))


# Service & Service Group association endpoints
@router.post("/service-service-group-associations")
async def create_service_group_association(
    fk_serviceid: int, fk_service_grouno: int, db: AsyncSessionDep
):
    return await ServiceServiceGroupAssociation(fk_service_grouno=fk_service_grouno, fk_serviceid=fk_serviceid).save(db)


# Sync Service endpoints
@router.get("/sync")
async def sync_service_data(service_group_no: int, db: AsyncSessionDep):
    services = (await ServiceGroup.find(db, with_eager_loading=True, no=service_group_no)).services
    for service in services:
        await db.refresh(service, ["service_price"])
    return services

