from datetime import datetime
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class CommentBase(BaseModel):
    content: str


class Comment(CommentBase):
    id: int
    post_id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class CommentCreate(CommentBase):
    post_id: int


class CommentUpdate(CommentBase):
    pass
