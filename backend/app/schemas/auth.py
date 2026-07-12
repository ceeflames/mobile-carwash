from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserRegister(BaseModel):
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(min_length=10, max_length=20)
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    phone: str
    is_active: bool
    email_verified: bool
    phone_verified: bool

    model_config = {
        "from_attributes": True
    }