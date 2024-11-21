import pytz
from datetime import datetime, timedelta
from jose import jwt

from ..settings import settings


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    time_now = datetime.now(pytz.timezone("Europe/Moscow"))
    if expires_delta:
        expire = time_now + expires_delta
    else:
        expire = time_now + timedelta(minutes=settings.jwt.access_token_expire_minutes)
    to_encode.update({"exp": expire, "iat": time_now})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt.secret_key, algorithm=settings.jwt.algorithm
    )
    return encoded_jwt
