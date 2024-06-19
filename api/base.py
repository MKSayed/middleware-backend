from api.deps import SessionDep
from typing import List


class RouteBase:
    def __init__(
        self,
        *,
        model_name: str,
        crud_model,
        pk_name: str | None = None,
        base_model,
        router,
        create=True,
        get_all=True,
        update=True,
    ):

        if create:

            @router.post(f"/new-{model_name}")
            def create(request: base_model, db: SessionDep):
                return crud_model.create(db, obj_in=request)

        if get_all:

            @router.get(f"/all-{model_name}s", response_model=List[base_model])
            async def get_all(db: SessionDep):
                return crud_model.get_all(db)

        if update and pk_name is not None:

            @router.put(f"/update-{model_name}/{{pk}}")
            async def update(pk, request: base_model, db: SessionDep):
                db_obj = crud_model.get_model_by_attribute(db, pk_name, pk)
                return crud_model.update(db, db_obj=db_obj, obj_in=request)
