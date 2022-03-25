import datetime
from fastapi import Request, HTTPException, status
import hashlib

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_LIFETIME
from jose import jwt


def hash_passwd(raw_password: str) -> str:
    password = hashlib.sha256(raw_password.encode(encoding='utf-8')).hexdigest()
    return password


def verify_password(password: str, hashed_password: str) -> bool:
    return hashlib.sha256(password.encode(encoding='utf-8')).hexdigest() == hashed_password


def create_access_token(username: str) -> str:
    to_encode = {"sub": username}
    to_encode.update({"exp": datetime.datetime.now() + datetime.timedelta(minutes=ACCESS_TOKEN_LIFETIME)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        encoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.JWSError:
        return
    return encoded_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        exp = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid auth token")
        if credentials:
            token = decode_access_token(credentials.credentials)
            if token is None:
                raise exp
            return credentials.credentials
        else:
            raise exp
