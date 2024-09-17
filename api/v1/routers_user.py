from fastapi import APIRouter, HTTPException, status

from sqlalchemy.exc import IntegrityError

from api.deps import AsyncSessionDep, CurrentUserDep
from schemas.schemas_user import (
    UserCreate,
    UserUpdate,
    UserDisplay,
)
from models.models_user import User
from core.security import get_password_hash

router = APIRouter()


@router.get("/users", response_model=list[UserDisplay])
async def get_all_users(db: AsyncSessionDep, current_user: CurrentUserDep):
    return await User.get_all(db)


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(request: UserCreate, db: AsyncSessionDep):

    user_dict = request.model_dump()
    user_dict["password"] = get_password_hash(user_dict["password"])
    try:
        return await User(**user_dict).save(db)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )


@router.put("/users/{pk}", response_model=UserDisplay)
async def update_user(pk: int, db: AsyncSessionDep, user_update: UserUpdate):
    update_dict = user_update.model_dump(exclude_unset=True)

    # Hash the new password before saving in database
    if password := update_dict.get("password"):
        update_dict["password"] = get_password_hash(password)
    else:
        # Make sure no empty string is being sent to database
        try:
            del update_dict["password"]
        except KeyError:
            pass

    try:
        updated_user = await User.find(db, id=pk)
        return await updated_user.update(db, **update_dict)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Failed to update user"
        )
