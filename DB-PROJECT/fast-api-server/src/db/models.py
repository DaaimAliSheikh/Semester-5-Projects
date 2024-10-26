from sqlmodel import SQLModel, Field, Column  # type: ignore
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
import uuid


class User(SQLModel, table=True):
    __tablename__: str = "users"  # type: ignore

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    username: str = Field(sa_column=Column(
        pg.VARCHAR(255),
        nullable=False,
        unique=False
    ))
    email: str = Field(sa_column=Column(
        pg.VARCHAR(255),
        nullable=False,
        unique=True
    ))
    password_hash: str = Field(sa_column=Column(
        pg.VARCHAR(255),
        nullable=False
    ), exclude=True)
    is_verified: bool = Field(sa_column=Column(
        pg.BOOLEAN,
        nullable=False,
        default=False
    ))
    profile_picture_url: str = Field(sa_column=Column(
        pg.VARCHAR(255),
        nullable=True
    ))
    created_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now))

    def __repr__(self):
        return f"<User {self.id}, username: {self.username}>"


class Book(SQLModel, table=True):
    __tablename__: str = "books"  # type: ignore

    ISBN_NO: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    Title: str = Field(sa_column=Column(
        pg.VARCHAR(255),
        nullable=False
    ))
    Author: str = Field(sa_column=Column(
        pg.VARCHAR(255),
        nullable=False
    ))
    created_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now))

    def __repr__(self):
        return f"<Book ISBN_NO: {self.ISBN_NO}, Title: {self.Title}, Author: {self.Author}>"
