from .extensions import db, login_manager
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class User(db.Model, UserMixin):

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    # แก้ตรงนี้
    firstname: Mapped[str] = mapped_column(String(30), nullable=True)
    lastname: Mapped[str] = mapped_column(String(30), nullable=True)

    avatar: Mapped[str] = mapped_column(String(50), default="avatar.png")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    fighters: Mapped[List["Fighter"]] = relationship(
        "Fighter",
        back_populates="user"
    )

    def __repr__(self):
        return f"<User {self.username}>"


class Division(db.Model):

    __tablename__ = "division"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    fighters: Mapped[List["Fighter"]] = relationship(
        "Fighter",
        back_populates="division"
    )

    def __repr__(self):
        return f"<Division {self.name}>"


class Fighter(db.Model):

    __tablename__ = "fighter"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    height: Mapped[str] = mapped_column(String(20), nullable=False)
    weight: Mapped[str] = mapped_column(String(20), nullable=False)

    age: Mapped[int] = mapped_column(Integer)
    country: Mapped[str] = mapped_column(String(100))
    team: Mapped[str] = mapped_column(String(100))

    description: Mapped[str] = mapped_column(Text)
    img_url: Mapped[str] = mapped_column(Text)

    division_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("division.id")
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="fighters"
    )

    division: Mapped["Division"] = relationship(
        "Division",
        back_populates="fighters"
    )

    def __repr__(self):
        return f"<Fighter {self.name}>"