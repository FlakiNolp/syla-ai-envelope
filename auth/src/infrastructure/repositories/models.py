from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, mapped_column, Mapped, DeclarativeBase

from infrastructure.repositories.values import (
    CreatedAt,
    UpdatedAt,
    ID,
)


class Base(DeclarativeBase):
    id: Mapped[ID]
    registered_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]


class User(Base):
    __tablename__ = "user"
    email: Mapped[str] = mapped_column(unique=True, nullable=False, comment="Почта пользователя")
    password: Mapped[str] = mapped_column(nullable=False, unique=False, comment="Хешированный пароль пользователя")
    chats: Mapped[list["Chat"]] = relationship(cascade="all", back_populates="user")


class Chat(Base):
    __tablename__ = "chat"
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[ID] = mapped_column(ForeignKey(User.id, ondelete="CASCADE", onupdate="CASCADE"))
    user: Mapped[User] = relationship(back_populates="chats")
