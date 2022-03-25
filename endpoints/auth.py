import datetime
from core.security import create_access_token, verify_password
from fastapi import APIRouter, HTTPException, status
from models.users import User, UserIn
from models.token import Token, Login
from db.models import User as DbUser
from db.base import get_session

router = APIRouter()


@router.post("/login", response_model=Token)
def login(login_data: Login):
    with get_session() as session:
        user = session.query(DbUser).where(DbUser.username == login_data.username).one_or_none()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="incorrect username or password")
    return Token(
        access_token=create_access_token(username=user.username)
    )
