from fastapi import Header
from fastapi import HTTPException

from typing import Annotated

import jwt

import os



class JWTTokenExceptionHandler:
    
    @classmethod
    def get_user_logged(cls, x_acess_token: Annotated[str, Header()]):
        """metod for get user logged form token"""
        if not 'bearer' in x_acess_token:
            cls.set_exception_http("invalid token bearer", 401)
        token_true = x_acess_token.replace("bearer ", "")
        try:
            FIELDS_ACCOUNT_LOGGED = jwt.decode(token_true, os.getenv("SECRET_KEY"), ["HS256"])
        except:
            cls.set_exception_http("your signature was expired", 401)
        return FIELDS_ACCOUNT_LOGGED
    
    @classmethod
    def set_exception_http(cls, detail_exception: str, status_code: int):
        """padronize http exceptions"""
        raise HTTPException(
            detail=detail_exception,
            status_code=status_code
        )
