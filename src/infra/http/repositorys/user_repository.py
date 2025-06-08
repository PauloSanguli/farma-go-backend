from typing import Type

from fastapi.exceptions import HTTPException
from sqlmodel import Session, select

from src.domain.schemas import PharmacySchema, UserSchema
from src.infra.configs import get_session
from src.infra.models import User


class UserRepository:
    def create_user(user_data: UserSchema) -> dict[str, str]:
        session: Session = get_session()
        user = User(email=user_data.email, name=user_data.email)
        user._encrypt_password(user_data.password)
        session.add(user)
        session.commit()
        session.close()
        return {"detail": "User created with sucessfuly"}

    def retrieve_profile_info(user_id: str) -> User:
        session: Session = get_session()
        user = session.get(User, user_id)
        user.image_url = "https://cdn.britannica.com/74/219774-050-E0858F86/Michael-B-Jordan-2019.jpg"
        result = user.search_history
        session.close()
        return result
