from fastapi import APIRouter
from api.deps import SessionDep
from db.controllers.user import user_controller
import schemas.schemas_user as user_schema
from crud.crud_user import crud_user

router = APIRouter()


@router.post("/new")
def create_user(request: user_schema.UserCreate, db: SessionDep):
    return crud_user.create(db, obj_in=request)


# @router.get('/', response_model=list[UserBase])
# def get_all_users(db: Session = Depends(get_db)):
#     return user_controller.get_all_users(db)
#
#
# @router.get('/{id}', response_model=UserBase)
# def get_user(id: int, db: Session = Depends(get_db)):
#     return user_controller.get_user(db, id)