from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

import bcrypt


db_user = 'gen_user'
db_password = 'testerai2023yoga'
db_host = '80.90.184.30'
db_name = 'default_db'
db_port = '5432'
db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

salt_rounds = 12


def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


def get_hashed_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=salt_rounds)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def verify_password(password: str, hashed_pass: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_pass.encode('utf-8'))


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    registered_at = Column(DateTime)
    password = Column(String, nullable=True)
    token_id = Column(String, nullable=True)

    name = Column(String)
    login = Column(String)
    github_id = Column(Integer, nullable=True)
    google_id = Column(String, nullable=True)

    jti = Column(String, nullable=True)

    messages = relationship("MessageOrm")
    tokens = relationship("UserTokens", uselist=False)


class GithubUserCreate(BaseModel):
    token: str
    login: str
    name: str
    github_id: str
    registered_at: str = Field(default=datetime.utcnow())


class UserCreate(BaseModel):
    email: str
    password: str
    registered_at: str = Field(default=datetime.utcnow())


class UserResponse(BaseModel):
    token_id: Optional[str]
    message: Optional[str]

    class Config:
        orm_mode = True


GPTTOKENS_DEFAULT = 1024
MESSAGECOUNT_DEFAULT = 5


class UserTokens(Base):
    __tablename__ = 'user_tokens'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column("user_id", Integer(),
                     ForeignKey("users.id"), nullable=False)
    tokens = Column(Integer, default=GPTTOKENS_DEFAULT)
    message_count = Column(Integer, default=MESSAGECOUNT_DEFAULT)

    user = relationship("User", back_populates="tokens", uselist=False)


class UserTokensSchema(BaseModel):
    tokens: int


class Message(BaseModel):
    question_id: int
    text: str

    class Config:
        orm_mode = True


class SignInRequest(BaseModel):
    email: str
    password: str


class SignInResponse(BaseModel):
    token_id: str
    messages: List[Message] = []

    class Config:
        orm_mode = True


class GoogleRegistrationCreate(BaseModel):
    email: str
    jti: str


class GoogleDataResponse(BaseModel):
    jti: Optional[str]
    message: str


class MessageOrm(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column("user_id", Integer(),
                     ForeignKey("users.id"), nullable=False)
    question_id = Column("question_id", Integer(),
                         ForeignKey("messages.id"), nullable=True)
    text = Column(String)
    type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow())

    user = relationship("User", back_populates="messages")
    answer = relationship("MessageOrm", remote_side=[id])


class MessageCreate(BaseModel):
    text: str
    created_at: str = Field(default=datetime.utcnow())


class UserMessageResponse(BaseModel):
    text: str


metadata = Base.metadata

Base.metadata.create_all(bind=engine)
