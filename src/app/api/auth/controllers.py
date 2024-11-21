import uuid
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from loguru import logger
from jose import jwt
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from .models import CreateUser, UserResponse
from ...external.postgres.utils import UserDAL
from ...external.postgres.models import User
from ...external.hashing import Hasher
from ...external.postgres.connection import get_session
from ...settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


async def _get_user_by_user_id_for_auth(
    user_id: uuid.UUID, session: AsyncSession
) -> User | None:
    user_dal = UserDAL(session)
    return await user_dal.get_user_by_user_id(user_id=user_id)


async def _get_user_by_login_for_auth(login: str, session: AsyncSession) -> User | None:
    user_dal = UserDAL(session)
    return await user_dal.get_user_by_login(login=login)


async def authenticate_user(login: str, password: str, db: AsyncSession) -> User | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )
    if (user := await _get_user_by_login_for_auth(login=login, session=db)) is None:
        raise credentials_exception
    if not Hasher.verify_password(password, user.password):
        raise credentials_exception
    return user


async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)
) -> User | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError as exc:
        logger.error(str(exc))
        raise credentials_exception
    user = await _get_user_by_user_id_for_auth(user_id=user_id, session=db)
    if user is None:
        raise credentials_exception
    return user


async def create_user(body: CreateUser, session: AsyncSession) -> UserResponse | None:
    async with session.begin():
        user_dal = UserDAL(db_session=session)
        user = await user_dal.create_user(
            login=body.login, password=Hasher.get_password_hash(body.password)
        )
        if user is not None:
            return UserResponse(user_id=user.user_id)
