from models.models_connector import ModuleParameter, Module
from models.models_service import ServiceParameter, Service


def create_xml_base_structure(nsmap: dict) -> dict:
    """Create the basic XML structure with envelope, header, and body."""
    envelope = {"soapenv:Envelope": nsmap}

    return envelope


async def get_namespaces(db, service: Service, module: Module):
    namespace_parameters = list((await ModuleParameter.find_all(db, fk_module_id=module.id, fk_param_loc_cd=4))) + list((await ServiceParameter.find_all(db, fk_service_id=service.id, fk_param_loc_cd=4)))
    nsmap = {}
    for ns_param in namespace_parameters:
        nsmap[f"@{ns_param.key}"] = ns_param.value
    return nsmap
