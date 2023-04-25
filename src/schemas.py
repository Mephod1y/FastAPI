from datetime import datetime, date
from pydantic import BaseModel, EmailStr


class ContactModel(BaseModel):
    name: str
    second_name: str
    email: EmailStr
    phone: str
    born_day: date


class ContactResponse(BaseModel):
    id: int = 1
    name: str
    second_name: str
    email: EmailStr
    phone: str
    born_day: date
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True