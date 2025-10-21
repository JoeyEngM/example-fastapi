from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.types import conint
from datetime import datetime

"""
Those that use ORM mode: 
JSON → Database: No from_attributes needed (Pydantic receives dicts)
Database → JSON: YES from_attributes needed (Pydantic receives objects)
"""

#Schema:

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    #ORM MODE:
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut #We used the data stored in the USerOut schema!

    #ORM MODE:
    model_config = ConfigDict(from_attributes=True)

class PostOut(BaseModel):
    Post: Post
    votes: int

    #ORM MODE:
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]
    

class Vote(BaseModel): 
    post_id: int
    dir: conint(le=1) # type: ignore