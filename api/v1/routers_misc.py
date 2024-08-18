from fastapi import APIRouter, Query

from api.deps import AsyncSessionDep
from models.models_connector import Module, ModuleParameter
from models.models_service import Service, ServiceParameter

router = APIRouter()


@router.get("/all-parameters-by-service-id")
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
