from fastapi import HTTPException, Depends, status
from core.security import decode_access_token
from core.security import JWTBearer
from models.users import User
from db.models import User as DbUser
from db.base import get_session


def get_current_user(
    token: str = Depends(JWTBearer()),
) -> User:
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception
    username: str = payload.get("sub")
    if username is None:
        raise cred_exception

    with get_session() as session:
        user = session.query(DbUser).where(DbUser.username == username).one_or_none()

    if not user:
        raise cred_exception
    return User.object_parse(user)
