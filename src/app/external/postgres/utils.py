import uuid
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, login: str, password: str) -> User | None:
        new_user = User(login=login, password=password)
        try:
            self.db_session.add(new_user)
            await self.db_session.flush()
            await self.db_session.refresh(new_user)
            return new_user
        except IntegrityError:
            return

    async def get_user_by_login(self, login: str) -> User | None:
        query = select(User).where(User.login == login)
        user = await self.db_session.scalar(query)
        if user is not None:
            return user

    async def get_user_by_user_id(self, user_id: uuid.UUID) -> User | None:
        user = await self.db_session.get(User, user_id)
        if user is not None:
            return user
