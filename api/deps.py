from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from models.models_user import User
from jose import jwt

from core.config import settings
from crud.crud_user import crud_user
from database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(db: SessionDep, token: TokenDep) -> User:
    unauthorized_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail="Could not validate credentials",
                                           headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
    except (jwt.JWTError):
        raise unauthorized_exception
    user = crud_user.get_user_by_username(db, username=username)
    if not user:
        raise unauthorized_exception
    return user
