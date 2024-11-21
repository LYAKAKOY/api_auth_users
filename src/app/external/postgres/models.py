import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4(), server_default=uuid.uuid4().hex
    )
    login: Mapped[str] = mapped_column(String(15), unique=True, index=True)
    password: Mapped[str]
