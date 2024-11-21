from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from .models import Token, CreateUser, UserResponse
from .controllers import authenticate_user, create_user, get_current_user_from_token

from ...external.jwt import create_access_token
from ...external.postgres.models import User
from ...external.postgres.connection import get_session
from ...settings import settings

auth_user_router = APIRouter(prefix="/api", tags=["user"])


@auth_user_router.post("/reg", response_model=UserResponse)
async def reg_user(
    body: CreateUser, db: AsyncSession = Depends(get_session)
) -> UserResponse:
    user = await create_user(body, db)
    if user is None:
        raise HTTPException(status_code=422, detail="this login is already exists")
    return user


@auth_user_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    access_token_expires = timedelta(minutes=settings.jwt.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.user_id), "other_custom_data": []},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@auth_user_router.get("/current_user")
async def get_current_user(
    current_user: Annotated[User, Depends(get_current_user_from_token)],
):
    return current_user
