import time
from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from crud.crud_user import crud_user
from api.deps import SessionDep
from core.security import verify_password, create_access_token
from core.config import settings

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires: datetime


@router.post("", response_model=Token)
def login_access_token(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = crud_user.get_user_by_username(session, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expires = datetime.now() + access_token_expires
    return Token(access_token=create_access_token(data={"sub": user.username}, expires_delta=access_token_expires),
                 expires=expires)
