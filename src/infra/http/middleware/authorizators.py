import os
from typing import Annotated

import jwt
from fastapi import Header, HTTPException

from src.domain.enums import EntityRole
from src.infra.http.exceptions import InvalidTokenProvidedError, PermissionDeniedError


class JWTPermissionsHandler:
    @classmethod
    def get_admin_logged(cls, x_acess_token: Annotated[str, Header()]) -> dict[str, str]:
        """metod for get user logged form token"""
        admin_data: dict[str, str] = cls.__decode_token(x_acess_token)
        if EntityRole.ADMIN != admin_data.get("role"):
            raise PermissionDeniedError()
        return admin_data

    @classmethod
    def get_user_logged(cls, x_acess_token: Annotated[str, Header()]) -> dict[str, str]:
        """metod for get pharmacist logged form token"""
        user_data: dict[str, str] = cls.__decode_token(x_acess_token)
        if EntityRole.USER != user_data.get("role"):
            raise PermissionDeniedError()
        return user_data

    @classmethod
    def get_pharmacist_logged(cls, x_acess_token: Annotated[str, Header()]) -> dict[str, str]:
        """metod for get pharmacist logged form token"""
        pharmacist_data: dict[str, str] = cls.__decode_token(x_acess_token)
        if EntityRole.PHARMACIST != pharmacist_data.get("role"):
            raise PermissionDeniedError()
        return pharmacist_data
    
    @classmethod
    def __decode_token(cls, acess_token: str) -> dict[str, str]:
        """Method for decode token"""
        token_splited = acess_token.split(" ")
        if len(token_splited) != 2:
            cls.__raise_exception_http("invalid token bearer", 401)
        bearer, token = token_splited
        if "bearer" != bearer.lower():
            cls.__raise_exception_http("invalid token bearer", 401)
        try:
            data_decoded: dict[str, str] = jwt.decode(
                token, os.getenv("SECRET-KEY", ""), ["HS256"]
            )
        except (jwt.ExpiredSignatureError):
            raise InvalidTokenProvidedError()
        return data_decoded

    @classmethod
    def __raise_exception_http(cls, detail_exception: str, status_code: int):
        """padronize http exceptions"""
        raise HTTPException(detail=detail_exception, status_code=status_code)
