import os
from typing import Annotated

import jwt
from fastapi import Header, HTTPException

from src.domain.enums import EntityRole
from src.infra.http.exceptions import InvalidTokenProvidedError, PermissionDeniedError


class JWTPermissionsHandler:
    @classmethod
    def get_admin_logged(cls, x_acess_token: Annotated[str, Header()]):
        """metod for get user logged form token"""
        if not "bearer" in x_acess_token:
            cls.set_exception_http("invalid token bearer", 401)
        token_true = x_acess_token.replace("bearer ", "")
        try:
            admin_data = jwt.decode(token_true, os.getenv("SECRET-KEY", ""), ["HS256"])
            if EntityRole.ADMIN != admin_data.get("role"):
                raise PermissionDeniedError()
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            raise InvalidTokenProvidedError()
        return admin_data

    @classmethod
    def get_user_logged(cls, x_acess_token: Annotated[str, Header()]):
        """metod for get pharmacist logged form token"""
        if not "bearer" in x_acess_token:
            cls.set_exception_http("invalid token bearer", 401)
        token_true = x_acess_token.replace("bearer ", "")
        try:
            user_data = jwt.decode(token_true, os.getenv("SECRET-KEY", ""), ["HS256"])
            if EntityRole.USER != user_data.get("role"):
                raise PermissionDeniedError()
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            raise InvalidTokenProvidedError()
        return user_data

    @classmethod
    def get_pharmacist_logged(cls, x_acess_token: Annotated[str, Header()]):
        """metod for get pharmacist logged form token"""
        token_bearer = x_acess_token.lower()
        if not "bearer" in token_bearer:
            cls.set_exception_http("invalid token bearer", 401)
        token_true = token_bearer.replace("bearer ", "")
        try:
            pharmacist_data = jwt.decode(
                token_true, os.getenv("SECRET-KEY", ""), ["HS256"]
            )
            if EntityRole.PHARMACIST != pharmacist_data.get("role"):
                raise PermissionDeniedError()
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            raise InvalidTokenProvidedError()
        return pharmacist_data

    @classmethod
    def set_exception_http(cls, detail_exception: str, status_code: int):
        """padronize http exceptions"""
        raise HTTPException(detail=detail_exception, status_code=status_code)
