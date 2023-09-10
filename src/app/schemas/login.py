from dataclasses import dataclass
from typing import Optional
from fastapi import Form

from pydantic import (
    BaseModel,
    EmailStr
)


@dataclass
class LoginForm:
    email: str = Form(...)
    password: str = Form(...)


class JWTToken(BaseModel):
    access_token: str
    token_type: str


class JWTTokenPayload(BaseModel):
    sub: Optional[EmailStr] = None