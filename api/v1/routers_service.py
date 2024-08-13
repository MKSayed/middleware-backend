import httpx
from colorama import Fore, Style
from copy import deepcopy
import xmltodict

from fastapi import APIRouter, Query, status, HTTPException
from fastapi.responses import JSONResponse

from pydantic import TypeAdapter

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
    ServiceCreate,
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
    KioskServiceFlow,
)
from utils.xml_handler import create_xml_base_structure, add_module_parameters, add_service_parameters, \
    find_parameter_value, get_namespaces_url_timeout, remove_dataIdentifiers

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


# Service parameter type related endpoints
# @router.post("/service-parameter-types")
# async def create_service_parameter_type(
#     request: ServiceParameterTypeBase, db: AsyncSessionDep
# ):
#     return await ServiceParameterType(
#         **request.model_dump(exclude_unset=True, exclude_none=True)
#     ).save(db)
#
#
# @router.get("/service-parameter-types", response_model=list[ServiceParameterTypeBase])
# async def get_all_service_parameter_types(db: AsyncSessionDep):
#     return await ServiceParameterType.get_all(db)
#
#
# @router.put("/service-parameter-type/{pk}")
# async def update_service_parameter_type(
#     pk, request: ServiceParameterTypeBase, db: AsyncSessionDep
# ):
#     service_parameter_type = await ServiceParameterType.find(db, cd=pk)
#     return await service_parameter_type.update(
#         db, **request.model_dump(exclude_unset=True, exclude_none=True)
#     )


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
            include={"ar_name", "eng_name", "fk_module_id", "fk_provider_id"}
        )
    ).save(db, auto_commit=True)
    service_price_request_dict = request.model_dump(
        exclude={"ar_name", "eng_name", "fk_module_id", "fk_provider_id"}
    )
    service_price_request_dict["fk_service_id"] = service.id

    # rename price_type to type
    service_price_request_dict["type"] = service_price_request_dict.pop("price_type")

    try:
        service_price = await ServicePrice(**service_price_request_dict).save(db)
    except Exception as e:
        print(Fore.RED + str(e.with_traceback(None)) + Style.RESET_ALL)
        await db.rollback()
        await db.delete(service)
        await db.commit()
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
    services = await Service.get_all(db, with_eager_loading=True)
    if short:
        short_services_adapter = TypeAdapter(list[ServiceDisplayShort])
        return short_services_adapter.validate_python(services)
    return services


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
            if param.nest_level == 0 or param.fk_service_para_type_cd == 3:
                root_parameters.append(param)
                parameter_collection[param.ser] = param
            else:
                if hasattr(parameter_collection[param.parent_ser], "children"):
                    parameter_collection[param.parent_ser].children.append(param)
                    parameter_collection[param.ser] = param
                else:
                    parameter_collection[param.parent_ser].children = [param]
                    parameter_collection[param.ser] = param

        return {"service_name": service.eng_name, "service_parameters": root_parameters}
    return service_parameters


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


# Service parameter related endpoints
@router.post("/service-parameters")
async def create_service_parameter(request: ServiceParameterBase, db: AsyncSessionDep):
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
    service_parameter = await ServiceParameter.find(db, ser=pk)
    return await service_parameter.update(db, **request.model_dump(exclude_unset=True))


# Service & Service Group association endpoints
@router.post("/service-service-group-associations")
async def create_service_group_association(
    fk_serviceid: int, fk_service_grouno: int, db: AsyncSessionDep
):
    return await ServiceServiceGroupAssociation(
        fk_service_grouno=fk_service_grouno, fk_serviceid=fk_serviceid
    ).save(db)


# Sync Service endpoints
@router.get("/db-version")
async def get_db_version(db: AsyncSessionDep):
    return {"db_ver": 1}


@router.get("/sync")
async def sync_service_data(service_group_no: int, db: AsyncSessionDep):
    kiosk_services = await KioskService.get_all(db)
    kiosk_service_flows = await KioskServiceFlow.get_all(db)
    services = (
        await ServiceGroup.find(db, with_eager_loading=True, no=service_group_no)
    ).services

    for service in services:
        # Load service_price and service_parameters of each service
        # service_price and service_parameters are lazy loaded by default
        await db.refresh(service, ["service_price", "service_parameters"])

    return {
        "kiosk_services": kiosk_services,
        "kiosk_service_flows": kiosk_service_flows,
        "services": services,
    }


@router.post("/send_third_party_request")
async def send_third_party_request(service_id: int, db: AsyncSessionDep, data: dict):
    service = await Service.find(db, id=service_id)
    # service_parameters = await service.awaitable_attrs.service_parameters
    # input_service_parameters = [param for param in service_parameters if int(param.fk_service_para_typecd) in (1, 3)]
    input_service_parameters = list(await ServiceParameter.find_all(db, fk_serviceid=service_id, fk_service_para_type_cd=[1, 3]))
    module = await Module.find(db, with_eager_loading=True, id=1)

    # Copy the input_service_parameters and module objects to avoid modifying the original objects in the database
    copied_input_service_parameters = deepcopy(input_service_parameters)
    copied_module = deepcopy(module)

    # Populate parameter values
    for parameter in copied_input_service_parameters:
        parameter.value = find_parameter_value(data, parameter)

    if not copied_module.is_xml:
        # TODO: Add JSON logic
        pass
    else:
        nsmap, url, timeout = get_namespaces_url_timeout(copied_module.module_params)

        envelope, header, body = create_xml_base_structure(nsmap)

        await add_module_parameters(header, copied_module.module_params, db)
        await add_service_parameters(header, body, copied_input_service_parameters, db)

        remove_dataIdentifiers(envelope)

        # Send the request to the third party service provider
        async with httpx.AsyncClient() as client:
            # Had to use conditional to avoid setting the timeout as None since it is not the same
            # as the default value in httpx
            if timeout:
                response = await client.post(url, content=xmltodict.unparse(envelope), timeout=int(timeout))
            else:
                print(xmltodict.unparse(envelope, full_document=False))
                response = await client.post(url, content=xmltodict.unparse(envelope, full_document=False))

        if not response.is_success:
            raise HTTPException(status_code=response.status_code, detail=xmltodict.parse(response.text, xml_attribs=False))
        else:
            envelope = xmltodict.parse(response.text, xml_attribs=False)["soapenv:Envelope"]
            if "soapenv:Header" in envelope:
                header = envelope["soapenv:Header"]
            body = envelope["soapenv:Body"]
            header.update(body)
            return header

        # return {"done": True, "xml": response}
