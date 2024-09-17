from colorama import Fore, Style

from fastapi import APIRouter, Query, status, HTTPException
from fastapi.responses import JSONResponse

from pydantic import TypeAdapter, BaseModel

from api.deps import AsyncSessionDep
from models.models_connector import Module, ModuleParameter


from schemas.schemas_service import (
    ServiceBase,
    ServiceGroupBase,
    ServicePriceBase,
    CurrencyBase,
    ProviderBase,
    ServiceChargeBase,
    ServiceParameterBase,
    ServiceDisplayShort,
    CurrencyDisplayShort,
    ServiceDisplay,
    ServiceCreate, ServiceParameterCreate, HTTPMethodEnum, PriceListBase
)
from models.models_service import (
    Currency,
    Provider,
    ServiceParameter,
    ServiceCharge,
    ServiceServiceGroupAssociation,
    Service,
    ServiceGroup,
    ServicePrice,
    KioskService,
    KioskServiceFlow, PriceList,
)
from utils.service_module_params_utils import build_parameter_tree, attach_ids_and_values, replace_tuples_with_values, \
    get_root_parameters_nodes
from utils.xml_handler import create_xml_base_structure, get_namespaces

router = APIRouter()


# Currencies related endpoints
@router.post("/currencies")
async def create_currency(request: CurrencyBase, db: AsyncSessionDep):
    return await Currency(
        **request.model_dump(exclude_unset=True, exclude_none=True)
    ).save(db)


@router.get(
    "/currencies", response_model=list[CurrencyBase | CurrencyDisplayShort]
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
    return await currency.update(
        db, **request.model_dump(exclude_unset=True, exclude_none=True)
    )


# Providers related endpoints
@router.post("/providers")
async def create_provider(request: ProviderBase, db: AsyncSessionDep):
    return await Provider(
        **request.model_dump(exclude_unset=True, exclude_none=True)
    ).save(db)


@router.get("/providers", response_model=list[ProviderBase])
async def get_all_providers(db: AsyncSessionDep):
    return await Provider.get_all(db)


@router.put("/providers/{pk}")
async def update_provider(pk: int, request: ProviderBase, db: AsyncSessionDep):
    provider = await Provider.find(db, id=pk)
    return await provider.update(
        db, **request.model_dump(exclude_unset=True, exclude_none=True)
    )


@router.get("/providers/{pk}/services")
async def get_provider_services(pk: int, db: AsyncSessionDep):
    return await Service.find(db, fk_providerid=pk)


# Service group related endpoints
@router.post("/service-groups")
async def create_service_group(request: ServiceGroupBase, db: AsyncSessionDep):
    return await ServiceGroup(
        **request.model_dump(exclude_unset=True, exclude_none=True)
    ).save(db)


@router.get("/service-groups", response_model=list[ServiceGroupBase])
async def get_all_service_groups(db: AsyncSessionDep):
    return await ServiceGroup.get_all(db)


@router.put("/service-groups/{pk}")
async def update_service_group(pk, request: ServiceGroupBase, db: AsyncSessionDep):
    service_group = await ServiceGroup.find(db, no=pk)
    return await service_group.update(
        db, **request.model_dump(exclude_unset=True, exclude_none=True)
    )


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
    service = await Service(
        **request.model_dump(
            include={"ar_name", "eng_name", "fk_module_id", "fk_provider_id", "http_method", "endpoint_path"}
        )
    ).save(db, auto_commit=True)
    service_price_request_dict = request.model_dump(
        exclude={"ar_name", "eng_name", "fk_module_id", "fk_provider_id", "http_method", "endpoint_path", "price_lists"}
    )
    service_price_request_dict["fk_service_id"] = service.id

    # rename price_type to type
    service_price_request_dict["type"] = service_price_request_dict.pop("price_type")

    try:
        service_price = await ServicePrice(**service_price_request_dict).save(db, auto_commit=True)
        # create the price_lists attached to the request's payload if price_type is 'LIST'
        if service_price.type == 'LIST':
            price_lists = request.model_dump(include={"price_lists"})["price_lists"]
            for price_list in price_lists:
                price_list["fk_service_price_id"] = service_price.id

            await PriceList.create_all(db, price_lists)
            await db.commit()
    except Exception as e:
        # If creation of a service_price or price_list failed, make sure to delete the created service and/or service_price
        print(Fore.RED + str(e.with_traceback(None)) + Style.RESET_ALL)
        await db.rollback()
        await db.delete(service)
        # Check if service_price was created and the exception occurred while creating price_lists or not
        try:
            if service_price:
                await db.delete(service_price)
        except NameError:
            pass
        await db.commit()
        raise HTTPException(detail="An error occurred while creating service", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    services = await Service.get_all(db, with_eager_loading=True)
    if short:
        short_services_adapter = TypeAdapter(list[ServiceDisplayShort])
        return short_services_adapter.validate_python(services)
    return services


@router.get("/services/{pk}", response_model=ServiceDisplay | ServiceDisplayShort)
async def get_all_services(
        pk:int,
    db: AsyncSessionDep,
    short: bool | None = Query(
        False, description="Whether to return the short version of the data"
    ),
):
    service = await Service.find(db, id=pk)
    if short:
        short_services_adapter = TypeAdapter(ServiceDisplayShort)
        return short_services_adapter.validate_python(service)
    return service


@router.put("/services/{pk}")
async def update_service(pk, request: ServiceBase, db: AsyncSessionDep):
    service = await Service.find(db, id=pk)
    return await service.update(db, **request.model_dump(exclude_unset=True))


@router.get("/services/{pk}/parameters")
async def get_all_params_for_service(pk: int, db: AsyncSessionDep, nested_form: bool = Query()):
    service = await Service.find(db, id=pk)
    service_parameters = await ServiceParameter.find_all(db, fk_service_id=pk)

    if nested_form:
        root_parameters = []
        parameter_collection = {}
        for param in sorted(service_parameters, key=lambda x: int(x.nest_level)):
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

        return {"service_name": service.eng_name, "service_parameters": root_parameters}
    return service_parameters


@router.get("/services/{pk}/combined-parameters")
async def get_all_module_params_for_service(pk: int, db: AsyncSessionDep, nested_form: bool = Query()):
    service = await Service.find(db, id=pk)
    module = await Module.find(db, id=service.fk_module_id)

    service_params_search_criteria = {"fk_service_id": service.id}
    module_params_search_criteria = {"fk_module_id": module.id}

    if not nested_form:
        # Remove xml name space parameters
        service_params_search_criteria.update({"not_fk_param_loc_cd": 4})
        module_params_search_criteria.update({"not_fk_param_loc_cd": 4})

    service_parameters = await ServiceParameter.find_all(db, **service_params_search_criteria)
    module_parameters = await ModuleParameter.find_all(db, **module_params_search_criteria)

    combined_parameters = list(service_parameters) + list(module_parameters)

    if nested_form:
        root_parameters = []
        parameter_collection = {}
        for param in sorted(combined_parameters, key=lambda x: int(x.nest_level)):
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

        return root_parameters
    return {"module_parameters": module_parameters, "service_parameters": service_parameters, "is_xml": module.is_xml}


# Service price related endpoints
@router.post("/service-prices")
async def create_service_price(request: ServicePriceBase, db: AsyncSessionDep):
    return await ServicePrice(
        **request.model_dump(exclude_unset=True, exclude_none=True)
    ).save(db)


@router.get("/service-prices", response_model=list[ServicePriceBase])
async def get_all_service_prices(db: AsyncSessionDep):
    return await ServicePrice.get_all(db)


@router.put("/service-prices/{pk}")
async def update_service_price(pk, request: ServicePriceBase, db: AsyncSessionDep):
    service_price = await ServicePrice.find(db, id=pk)
    return await service_price.update(
        db, **request.model_dump(exclude_none=True, exclude_unset=True)
    )


# Price list related endpoints
@router.post("/price_lists")
async def create_price_list(request: PriceListBase, db: AsyncSessionDep):
    return await PriceList(
        **request.model_dump(exclude_unset=True)
    ).save(db)


@router.get("/price_lists", response_model=list[PriceListBase])
async def get_all_price_lists(db: AsyncSessionDep):
    return await PriceList.get_all(db)


@router.put("/price_lists/{pk}")
async def update_price_list(pk, request: PriceListBase, db: AsyncSessionDep):
    price_list = await PriceList.find(db, id=pk)
    return await price_list.update(
        db, **request.model_dump(exclude_none=True, exclude_unset=True)
    )


# Service parameter related endpoints
@router.post("/service-parameters")
async def create_service_parameter(request: ServiceParameterCreate, db: AsyncSessionDep):
    return await ServiceParameter(
        **request.model_dump(exclude_unset=True, exclude_none=True)
    ).save(db)


@router.get("/service-parameters", response_model=list[ServiceParameterBase])
async def get_all_service_parameters(db: AsyncSessionDep):
    return await ServiceParameter.get_all(db)


@router.put("/service-parameters/{pk}")
async def update_service_parameter(
    pk, request: ServiceParameterBase, db: AsyncSessionDep
):
    service_parameter = await ServiceParameter.find(db, id=pk)
    return await service_parameter.update(db, **request.model_dump(exclude_unset=True))


@router.delete('/service-parameters/{pk}')
async def delete_service_parameter(pk, db: AsyncSessionDep):
    service_parameter = await ServiceParameter.find(db, id=pk)
    await service_parameter.delete_self(db, auto_commit=True)
    return {"detail": 'success'}


# Service & Service Group association endpoints
@router.post("/service-service-group-associations")
async def create_service_group_association(
    fk_service_id: int, fk_service_group_no: int, db: AsyncSessionDep
):
    return await ServiceServiceGroupAssociation(
        fk_service_group_no=fk_service_group_no, fk_service_id=fk_service_id
    ).save(db)

