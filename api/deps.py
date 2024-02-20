from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends

from database import get_db

SessionDep = Annotated[Session, Depends(get_db)]

