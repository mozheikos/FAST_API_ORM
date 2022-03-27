import datetime
from core.security import hash_passwd
from fastapi import APIRouter, Depends, HTTPException, status
from models.users import User, UserIn, UpdatedUser
from typing import List
import db.models as db
from db.base import get_session
from endpoints.depends import get_current_user

router = APIRouter()


@router.get("/", response_model=List[User])
def get_all(
        limit: int = 100,
        offset: int = 0):
    with get_session() as session:
        users_list = session.query(db.User).order_by(db.User.id).limit(limit=limit).offset(offset).all()

    result = []
    for item in users_list:
        result.append(User.object_parse(item))
    return result


@router.get("/id/", response_model=User)
def get_user_by_id(user_id: int):
    with get_session() as session:
        user = session.query(db.User).where(db.User.id == user_id).one_or_none()
    if user:
        return User.object_parse(user)
    return


@router.post("/create/", response_model=User)
def create_user(instance: UserIn):
    values = instance.dict()

    raw_password = values.pop("password", None)
    values.pop("password2", None)
    values['created_at'] = datetime.datetime.now()
    values['updated_at'] = datetime.datetime.now()
    values["hashed_password"] = hash_passwd(raw_password)

    user = User(**values)

    with get_session() as session:
        new_user = db.User(**values)
        session.add(new_user)
        session.commit()

        user.id = new_user.id
    return user


@router.put("/update/", response_model=User)
def update_user(
        instance: UpdatedUser,
        current_user: db.User = Depends(get_current_user)):

    with get_session() as session:

        if not current_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

        current_user.name = instance.name
        current_user.lastname = instance.lastname
        current_user.updated_at = datetime.datetime.now()
        session.add(current_user)
        session.commit()

        user = session.query(db.User).filter(db.User.id == current_user.id).one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        return User.object_parse(user)


@router.delete("/delete/")
def delete_user(
        current_user: db.User = Depends(get_current_user)):

    name = current_user.username

    with get_session() as session:

        session.delete(current_user)
        session.commit()

        return {"user": name}
