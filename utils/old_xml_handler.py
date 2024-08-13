from typing import Any

from bs4 import BeautifulSoup, Tag
from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.models_connector import Module, ModuleParameter
from models.models_service import ServiceParameter


def create_xml_base_structure(
    beautiful_soup_object: BeautifulSoup, nsmap: dict
) -> tuple[Tag, Tag, Tag]:
    """Create the basic XML structure with envelope, header, and body."""
    envelope = beautiful_soup_object.new_tag("soapenv:Envelope", **nsmap)
    header = beautiful_soup_object.new_tag("soapenv:Header")
    body = beautiful_soup_object.new_tag("soapenv:Body")
    envelope.append(header)
    envelope.append(body)
    return envelope, header, body


# Helper function to create XML elements
def create_xml_elements(soup, parent, key, value, id=None):
    if isinstance(value, dict):
        sub_element = soup.new_tag(key)
        sub_element.id = id
        parent.append(sub_element)
        for sub_key, sub_value in value.items():
            create_xml_elements(soup, sub_element, sub_key, sub_value)
    elif isinstance(value, list):
        for item in value:
            sub_element = soup.new_tag(key)
            sub_element.id = id
            if isinstance(item, dict):
                parent.append(sub_element)
                for sub_key, sub_value in item.items():
                    create_xml_elements(soup, sub_element, sub_key, sub_value)
            else:
                sub_element.string = str(item)
                parent.append(sub_element)
    else:
        sub_element = soup.new_tag(key)
        sub_element.id = id
        if value:
            sub_element.string = str(value)
        parent.append(sub_element)


def find(d, key):
    """
    Recursively searches for the first dictionary within the nested dictionary 'd' that contains the specified 'key'.
    Returns the first dictionary containing the key, or None if not found.
    """
    if not isinstance(d, dict):
        return None

    if key in d:
        return d

    for k, v in d.items():
        if isinstance(v, dict):
            result = find(v, key)
            if result is not None:
                return result
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    result = find(item, key)
                    if result is not None:
                        return result

    return None


def find_all(d, key):
    """
    Recursively searches for all dictionaries within the nested dictionary 'd' that contain the specified 'key'.
    Returns a list of dictionaries containing the key.
    """
    if not isinstance(d, dict):
        return []

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
        else:
            return

    if len(data_list) == 1:
        return (
            None
            if isinstance(data_list[0][parameter.key], dict)
            else data_list[0][parameter.key]
        )

    return find_value_with_identifier(data_list, parameter)


def find_value_with_identifier(
    data_list: list[dict[str, Any]], parameter: ServiceParameter
) -> Any:
    """Find the value in a list of dictionaries using the dataIdentifier."""
    for item in data_list:
        try:
            if int(item["dataIdentifier"]) == int(parameter.parent_ser):
                return (
                    None
                    if isinstance(item[parameter.key], dict)
                    else item[parameter.key]
                )
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


async def add_module_parameters(
    beautiful_soup_object: BeautifulSoup,
    header: Tag,
    module_params: list[ModuleParameter],
    db: AsyncSession,
):
    """Add module parameters to the XML structure."""
    for current_module_param in sorted(module_params, key=lambda x: int(x.nest_level)):
        if current_module_param.nest_level == 0:
            create_xml_elements(
                beautiful_soup_object,
                header,
                current_module_param.key,
                current_module_param.value,
                id=current_module_param.id,
            )
        else:
            await add_nested_parameter(
                beautiful_soup_object, header, current_module_param, db
            )


async def add_service_parameters(
    beautiful_soup_object: BeautifulSoup,
    header: Tag,
    body: Tag,
    input_service_parameters: list[ServiceParameter],
    db: AsyncSession,
):
    """Add service parameters to the XML structure."""
    for current_service_param in sorted(
        input_service_parameters, key=lambda x: int(x.nest_level)
    ):
        head_or_body = (
            header if int(current_service_param.fk_service_para_type_cd) == 3 else body
        )
        if current_service_param.nest_level == 0:
            create_xml_elements(
                beautiful_soup_object,
                head_or_body,
                current_service_param.key,
                current_service_param.value,
                id=current_service_param.ser,
            )
        else:
            await add_nested_parameter(
                beautiful_soup_object, head_or_body, current_service_param, db
            )


async def get_parent_param(
    db: AsyncSession,
    current_param: ServiceParameter | ModuleParameter,
):
    """Retrieve the parent parameter based on the current parameter and parent tag."""
    if isinstance(current_param, ServiceParameter):
        if current_param.fk_service_para_type_cd == 3:
            return await ModuleParameter.find(db, id=current_param.parent_ser)
        else:
            return await ServiceParameter.find(db, ser=current_param.parent_ser)
    else:  # ModuleParameter
        return await ModuleParameter.find(db, id=current_param.parent_id)


async def add_nested_parameter(
    beautiful_soup_object: BeautifulSoup,
    parent_tag: Tag,
    current_param: ServiceParameter | ModuleParameter,
    db: AsyncSession,
):
    """Add a nested parameter (either service or module) to the XML structure."""

    parent_param = await get_parent_param(db, current_param)
    parent_list = parent_tag.find_all(parent_param.key)

    if len(parent_list) == 1:
        create_xml_elements(
            beautiful_soup_object,
            parent_list[0],
            current_param.key,
            current_param.value,
            id=current_param.ser
            if isinstance(current_param, ServiceParameter)
            else current_param.id,
        )
    elif len(parent_list) == 0:
        raise HTTPException(
            detail=f"Element {current_param.key} was expected to be placed under {parent_param.key} but {parent_param.key} was not found in the xml structure",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    else:
        for parent in parent_list:
            if parent.id == (
                parent_param.ser
                if isinstance(current_param, ServiceParameter)
                else parent_param.id
            ):
                create_xml_elements(
                    beautiful_soup_object,
                    parent,
                    current_param.key,
                    current_param.value,
                    id=current_param.ser
                    if isinstance(current_param, ServiceParameter)
                    else current_param.id,
                )
                break
        else:
            raise HTTPException(
                detail=f"Expected a dataIdentifier that matches {parent_param.ser if isinstance(current_param, ServiceParameter) else parent_param.id} "
                       f"in one of the items since {parent_param.key} was present twice in received data",
                status_code=status.HTTP_400_BAD_REQUEST,
            )


def get_namespaces_url_timeout(module_parameters: list[ModuleParameter]):
    nsmap = {}
    url = None
    timeout = None
    elements_to_remove = []
    for module_param in module_parameters:
        if module_param.key.startswith("xmlns:"):
            nsmap[module_param.key] = module_param.value
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
