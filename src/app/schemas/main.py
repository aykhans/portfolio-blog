from dataclasses import dataclass
from typing import Optional

from fastapi import Form

from pydantic import EmailStr


@dataclass
class SendEmail:
    name: str = Form(..., max_length=50)
    email: EmailStr = Form(...)
    phone: Optional[str] = Form(None, max_length=20)
    message: str = Form(..., max_length=1000)