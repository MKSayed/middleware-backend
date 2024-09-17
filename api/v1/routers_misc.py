import httpx
import xmltodict
from fastapi import APIRouter, Query, HTTPException

from api.deps import AsyncSessionDep
from models.models_connector import Module, ModuleParameter
from models.models_service import Service, ServicePrice
from schemas.schemas_service import HTTPMethodEnum, ServicePriceTypeEnum

from utils.service_module_params_utils import build_parameter_tree, attach_ids_and_values, replace_tuples_with_values, \
    get_root_parameters_nodes
from utils.xml_handler import create_xml_base_structure, get_namespaces


global_session_data_collection = {}
router = APIRouter()


# It is in misc because it belongs to both module and service parameters
@router.get("/all-parameters-by-service-id", description="Returns both Service parameters and module parameters for a specific service")
async def get_all_parameters_by_service_id(db: AsyncSessionDep, service_id: int = Query()):
    service = await Service.find(db, id=service_id)
    services = await Service.find_all(db, with_eager_loading=True, fk_module_id=service.fk_module_id)
    module = await Module.find(db, id=service.fk_module_id)

    service_parameters = []
    for current_service in services:
        service_parameters.extend(current_service.service_parameters)

    module_parameters = await ModuleParameter.find_all(db, fk_module_id=service.fk_module_id)

    # combined_parameters = list(service_parameters) + list(module_parameters)

    return {"module_parameters": module_parameters, "service_parameters": service_parameters}


# @router.get("/db-version")
# async def get_db_version(db: AsyncSessionDep):
#     return {"db_ver": 1}


# @router.get("/sync")
# async def sync_service_data(service_group_no: int, db: AsyncSessionDep):
#     kiosk_services = await KioskService.get_all(db)
#     kiosk_service_flows = await KioskServiceFlow.get_all(db)
#     services = (
#         await ServiceGroup.find(db, with_eager_loading=True, no=service_group_no)
#     ).services
#
#     for service in services:
#         # Load service_price and service_parameters of each service
#         # service_price and service_parameters are lazy loaded by default
#         await db.refresh(service, ["service_price", "service_parameters"])
#
#     return {
#         "kiosk_services": kiosk_services,
#         "kiosk_service_flows": kiosk_service_flows,
#         "services": services,
#     }


@router.post("/send-third-party-request")
async def send_third_party_request(service_id: int, db: AsyncSessionDep, data: dict):
    # Fetch the requested service
    service = await Service.find(db, id=service_id)
    module = await Module.find(db, id=service.fk_module_id)
    # # Fetch input service parameters
    # # not_fk_param_loc_cd=4 prevents adding the xml namespaces as request body parameters
    # input_service_parameters = list(
    #     await ServiceParameter.find_all(db, fk_service_id=service_id, fk_param_type_cd=1, not_fk_param_loc_cd=4))
    #
    # # not_fk_param_loc_cd=4 prevents adding the xml namespaces as request body parameters
    # input_module_parameters = list(await ModuleParameter.find_all(db, fk_module_id=module.id, fk_param_type_cd=1, not_fk_param_loc_cd=4))
    #
    # # Sort the input service and module parameters ascending by next_level
    # input_service_parameters = sorted(input_service_parameters, key=lambda x: int(x.nest_level))
    # input_module_parameters = sorted(input_module_parameters, key=lambda x: int(x.nest_level))
    # # Combine input module parameters with input service parameters
    # # input module parameters should be first to be created as ParameterNodes firstly while building the parameter tree
    # input_parameters = input_module_parameters + input_service_parameters
    #
    # # Build parameter tree
    # root_nodes = build_parameter_tree(input_parameters)

    # Fetch input service parameters
    # not_fk_param_loc_cd=4 prevents adding the xml namespaces as request body parameters
    root_nodes = await get_root_parameters_nodes(db, service, module, fk_param_type_cd=1, not_fk_param_loc_cd=4)

    # get or create kiosk_session_data
    kiosk_id = 999  # Change the value of kiosk_id to the actual kiosk id in production
    if kiosk_id in global_session_data_collection:
        kiosk_session_data = global_session_data_collection[kiosk_id]
    else:
        global_session_data_collection[kiosk_id] = []
        kiosk_session_data = global_session_data_collection[kiosk_id]

    # Attach dataIdentifiers to every dictionary (except those nested inside lists) and extract
    # the corresponding the values from the request data dictionary using the node tree path
    result = {}
    for root_node in root_nodes.values():
        await attach_ids_and_values(db, data, root_node, result, kiosk_session_data)

    # Add the request's data to the global session data collection list for later use in next service calls that
    # requires the same input data without the need to pass it again from the client
    kiosk_session_data.append(result)

    # Convert tuples of (node_id, value) into value only after saving it in the session collection and before sending it to the external service
    input_dict = replace_tuples_with_values(result)

    if not module.is_xml:
        # TODO: Add JSON logic
        pass
    else:
        # Get the url and timeout from the module attributes and service attributes
        url = module.base_url + service.endpoint_path
        timeout = module.timeout
        nsmap = await get_namespaces(db, service, module)

        envelope = create_xml_base_structure(nsmap)
        envelope["soapenv:Envelope"].update(input_dict)

        print(xmltodict.unparse(envelope, full_document=False, pretty=True))

        # Send the request to the third party service provider
        async with httpx.AsyncClient() as client:
            # Had to use conditional to avoid setting the timeout as None since it is not the same
            # as the default value in httpx
            if timeout:
                # TODO handle the raised exception when timeout is met
                if service.http_method == HTTPMethodEnum.GET:
                    response = await client.get(url, content=xmltodict.unparse(envelope, full_document=False), timeout=int(timeout))
                elif service.http_method == HTTPMethodEnum.POST:
                    response = await client.post(url, content=xmltodict.unparse(envelope, full_document=False), timeout=int(timeout))
                elif service.http_method == HTTPMethodEnum.PUT:
                    response = await client.put(url, content=xmltodict.unparse(envelope, full_document=False), timeout=int(timeout))

        if not response.is_success:
            raise HTTPException(status_code=response.status_code, detail=xmltodict.parse(response.text, xml_attribs=False))
        response_dict = xmltodict.parse(response.text, xml_attribs=False)["soapenv:Envelope"]

        root_nodes = await get_root_parameters_nodes(db, service, module, fk_param_type_cd=2)

        result = {}
        for root_node in root_nodes.values():
            await attach_ids_and_values(db, response_dict, root_node, result, kiosk_session_data)

        kiosk_session_data.append(result)

        response_dict = replace_tuples_with_values(result)

        # Uncomment this line to Check the response on swagger if needed to make the creation of the output parameters easier
        # return xmltodict.parse(response.text, xml_attribs=False)


@router.get('payment-amount')
async def get_payment_amount(db: AsyncSessionDep, service_id: int, key: str | None = Query(None, description="required only if the required service's price is of type \"LIST\"")):
    # Todo this endpoint is to be updated to calculate the service charge as well when it is implemented
    service_price = await ServicePrice.find(db, fk_service_id=service_id)
    if service_price.type == ServicePriceTypeEnum.LIST:
        pass


@router.delete('kiosk-session')
def clear_kiosk_session_data(kiosk_id: int):
    del global_session_data_collection[kiosk_id]
