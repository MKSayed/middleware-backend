from typing import Any, Dict, Tuple

from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.models_connector import ModuleParameter
from models.models_service import ServiceParameter


def create_xml_base_structure(nsmap: dict) -> Tuple[Dict, Dict, Dict]:
    """Create the basic XML structure with envelope, header, and body."""
    envelope = {"soapenv:Envelope": nsmap}
    header = {"soapenv:Header": {}}
    body = {"soapenv:Body": {}}
    envelope["soapenv:Envelope"].update(header)
    envelope["soapenv:Envelope"].update(body)
    return envelope, header["soapenv:Header"], body["soapenv:Body"]


def create_xml_elements(parent: dict, key: str, value: Any, id: Any = None):
    if isinstance(value, dict):
        sub_element = {key: {"@dataIdentifier": id}}
        parent.update(sub_element)
        for sub_key, sub_value in value.items():
            create_xml_elements(sub_element[key], sub_key, sub_value)
    elif isinstance(value, list):
        parent[key] = []
        for item in value:
            sub_element = {"@dataIdentifier": id}
            if isinstance(item, dict):
                for sub_key, sub_value in item.items():
                    create_xml_elements(sub_element, sub_key, sub_value)
            else:
                sub_element["#text"] = str(item)
            parent[key].append(sub_element)
    else:
        parent[key] = {"@dataIdentifier": id, "#text": str(value) if value else None}


def find(d: dict, key: str) -> dict:
    """Recursively searches for the first dictionary within the nested dictionary 'd' that contains the specified 'key'."""
    if key in d:
        return d
    for k, v in d.items():
        if isinstance(v, dict):
            result = find(v, key)
            if result:
                return result
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    result = find(item, key)
                    if result:
                        return result
    return None


def find_all(d: dict, key: str) -> list:
    """Recursively searches for all dictionaries within the nested dictionary 'd' that contain the specified 'key'."""
    found = []
    if key in d:
        found.append(d)
    for k, v in d.items():
        if isinstance(v, dict):
            found.extend(find_all(v, key))
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    found.extend(find_all(item, key))
    return found


def find_parameter_value(data: dict[str, Any], parameter: ServiceParameter) -> Any:
    """Find the value for a given parameter in the input data."""
    data_list = find_all(data, parameter.key)
    if not data_list:
        if not parameter.is_optional:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Required Service Parameter {parameter.key} wasn't provided in request data. Received data: {data}",
            )
        return None

    if len(data_list) == 1:
        return data_list[0][parameter.key] if not isinstance(data_list[0][parameter.key], dict) else None

    return find_value_with_identifier(data_list, parameter)


def find_value_with_identifier(data_list: list[dict[str, Any]], parameter: ServiceParameter) -> Any:
    """Find the value in a list of dictionaries using the dataIdentifier."""
    for item in data_list:
        try:
            if int(item["dataIdentifier"]) == int(parameter.parent_ser):
                return item[parameter.key] if not isinstance(item[parameter.key], dict) else None
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Expected a dataIdentifier key in {item} since {parameter.key} was present twice in received data",
            )

    if not parameter.is_optional:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Expected a dataIdentifier that matches {parameter.parent_ser} in one of the items since {parameter.key} was present twice in received data",
        )


async def add_module_parameters(header: dict, module_params: list[ModuleParameter], db: AsyncSession):
    """Add module parameters to the XML structure."""
    for current_module_param in sorted(module_params, key=lambda x: int(x.nest_level)):
        if current_module_param.nest_level == 0:
            create_xml_elements(header, current_module_param.key, current_module_param.value, id=current_module_param.id)
        else:
            await add_nested_parameter(header, current_module_param, db)


async def add_service_parameters(header: dict, body: dict, input_service_parameters: list[ServiceParameter], db: AsyncSession):
    """Add service parameters to the XML structure."""
    for current_service_param in sorted(input_service_parameters, key=lambda x: int(x.nest_level)):
        head_or_body = header if int(current_service_param.fk_service_para_type_cd) == 3 else body
        if current_service_param.nest_level == 0:
            create_xml_elements(head_or_body, current_service_param.key, current_service_param.value, id=current_service_param.ser)
        else:
            await add_nested_parameter(head_or_body, current_service_param, db)


async def get_parent_param(db: AsyncSession, current_param: ServiceParameter | ModuleParameter):
    """Retrieve the parent parameter based on the current parameter and parent tag."""
    if isinstance(current_param, ServiceParameter):
        if current_param.fk_service_para_type_cd == 3:
            return await ModuleParameter.find(db, id=current_param.parent_ser)
        return await ServiceParameter.find(db, ser=current_param.parent_ser)
    return await ModuleParameter.find(db, id=current_param.parent_id)


async def add_nested_parameter(parent_tag: dict, current_param: ServiceParameter | ModuleParameter, db: AsyncSession):
    """Add a nested parameter (either service or module) to the XML structure."""
    parent_param = await get_parent_param(db, current_param)
    parent_list = find_all(parent_tag, parent_param.key)

    if len(parent_list) == 1:
        create_xml_elements(parent_list[0][parent_param.key], current_param.key, current_param.value, id=current_param.ser if isinstance(current_param, ServiceParameter) else current_param.id)
    elif len(parent_list) == 0:
        raise HTTPException(
            detail=f"Element {current_param.key} was expected to be placed under {parent_param.key} but {parent_param.key} was not found in the xml structure",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    else:
        for parent in parent_list:
            if parent.get("@dataIdentifier") == (parent_param.ser if isinstance(current_param, ServiceParameter) else parent_param.id):
                create_xml_elements(parent[parent_param.key], current_param.key, current_param.value, id=current_param.ser if isinstance(current_param, ServiceParameter) else current_param.id)
                break
        else:
            raise HTTPException(
                detail=f"Expected a dataIdentifier that matches {parent_param.ser if isinstance(current_param, ServiceParameter) else parent_param.id} in one of the items since {parent_param.key} was present twice in received data",
                status_code=status.HTTP_400_BAD_REQUEST,
            )


def get_namespaces_url_timeout(module_parameters: list[ModuleParameter]):
    nsmap = {}
    url = None
    timeout = None
    elements_to_remove = []
    for module_param in module_parameters:
        if module_param.key.startswith("xmlns:"):
            nsmap[f"@{module_param.key}"] = module_param.value
            elements_to_remove.append(module_param)
        elif module_param.key.startswith("connection."):
            if module_param.key.endswith(".url"):
                url = module_param.value
            if module_param.key.endswith(".timeout"):
                timeout = module_param.value
            elements_to_remove.append(module_param)

    for item in elements_to_remove:
        module_parameters.remove(item)

    return nsmap, url, timeout


def remove_dataIdentifiers(d):
    if isinstance(d, dict):
        if "@dataIdentifier" in d:
            del d["@dataIdentifier"]
        for value in d.values():
            remove_dataIdentifiers(value)
    elif isinstance(d, list):
        for item in d:
            remove_dataIdentifiers(item)
