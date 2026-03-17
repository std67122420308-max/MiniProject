from ONEChampionship.extensions import db, login_manager
from sqlalchemy import Integer, String, Text, Table, Column, DateTime, ForeignKey, func, Float
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
    avatar: Mapped[str] = mapped_column(String(25), default="avatar.png")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    fighters: Mapped[List["ONEChampionship"]] = relationship(
        back_populates="user"
    )

    def __repr__(self):
        return f"<User: {self.username}>"

one_team = Table(
    "one_team",
    db.metadata,
    Column("team_id", Integer, ForeignKey("team.id"), primary_key=True),
    Column("fighter_id", Integer, ForeignKey("onechampionship.id"), primary_key=True),
)


class Team(db.Model):

    __tablename__ = "team"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

    fighters: Mapped[List["ONEChampionship"]] = relationship(
        secondary=one_team,
        back_populates="teams"
    )

    def __repr__(self):
        return f"<Team: {self.name}>"


class ONEChampionship(db.Model):

    __tablename__ = "onechampionship"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[float] = mapped_column(Float, nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    weight_class: Mapped[str] = mapped_column(String(50), nullable=False)
    gym: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str] = mapped_column(Text, nullable=False)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    user: Mapped["User"] = relationship(
        back_populates="fighters"
    )

    teams: Mapped[List["Team"]] = relationship(
        secondary=one_team,
        back_populates="fighters"
    )

    def __repr__(self):
        return f"<Fighter: {self.name}>"