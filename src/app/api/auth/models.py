from uuid import UUID
from pydantic import BaseModel


class CreateUser(BaseModel):
    login: str
    password: str


class UserResponse(BaseModel):
    user_id: UUID


class Token(BaseModel):
    access_token: str
    token_type: str
