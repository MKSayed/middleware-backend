from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from models.models_user import User
from api.deps import AsyncSessionDep
from core.security import verify_password, create_access_token
from core.config import settings

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires: datetime
    username: str
    national_id: str


@router.post("", response_model=Token)
async def login_access_token(
    db: AsyncSessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await User.find(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expires = datetime.now() + access_token_expires
    return Token(
        access_token=create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        ),
        expires=expires,
        username=user.username,
        national_id=user.national_id,
    )
