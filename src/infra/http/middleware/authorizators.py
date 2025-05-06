import os
from typing import Annotated

import jwt
from fastapi import Header, HTTPException

from src.infra.http.exceptions import PermissionDeniedError, InvalidTokenProvidedError

class JWTTokenExceptionHandler:
    @classmethod
    def get_admin_logged(cls, x_acess_token: Annotated[str, Header()]):
        """metod for get user logged form token"""
        if not "bearer" in x_acess_token:
            cls.set_exception_http("invalid token bearer", 401)
        token_true = x_acess_token.replace("bearer ", "")
        try:
            admin_data = jwt.decode(
                token_true, os.getenv("SECRET-KEY", ""), ["HS256"]
            )
            if not "admin" == admin_data.get("role"):
                raise PermissionDeniedError()
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            cls.set_exception_http("your signature was expired or invalid", 401)
        return admin_data

    # @classmethod
    # def get_user_logged(cls, x_acess_token: Annotated[str, Header()]):
    #     """metod for get pharmacist logged form token"""
    #     if not "bearer" in x_acess_token:
    #         cls.set_exception_http("invalid token bearer", 401)
    #     token_true = x_acess_token.replace("bearer ", "")
    #     try:
    #         FIELDS_ACCOUNT_LOGGED = jwt.decode(
    #             token_true, os.getenv("SECRET-sKEY"), ["HS256"]
    #         )
    #     except:
    #         cls.set_exception_http("your signature was expired", 401)
    #     return FIELDS_ACCOUNT_LOGGED

    # @classmethod
    # def get__logged(cls, x_acess_token: Annotated[str, Header()]):
    #     """metod for get pharmacist logged form token"""
    #     if not "bearer" in x_acess_token:
    #         cls.set_exception_http("invalid token bearer", 401)
    #     token_true = x_acess_token.replace("bearer ", "")
    #     try:
    #         FIELDS_ACCOUNT_LOGGED = jwt.decode(
    #             token_true, os.getenv("SECRET-sKEY"), ["HS256"]
    #         )
    #     except:
    #         cls.set_exception_http("your signature was expired", 401)
    #     return FIELDS_ACCOUNT_LOGGED

    @classmethod
    def set_exception_http(cls, detail_exception: str, status_code: int):
        """padronize http exceptions"""
        raise HTTPException(detail=detail_exception, status_code=status_code)
