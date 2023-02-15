from datetime import datetime, date
from pydantic import BaseModel, Field

class ContactBase(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(max_length=50)
    phone: str = Field(max_length=50)
    birthday: date = Field(max_length=50)


class ContactModel(ContactBase):
    pass

class ContactUpdate(ContactModel):
    done: bool


class ContactResponse(ContactBase):
    id: int
    created: datetime

    class Config:
        orm_mode = True