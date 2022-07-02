from enum import Enum
from pydantic import BaseModel
from pydantic import EmailStr
from typing import List, Optional




class BookAuthors(BaseModel):
    book_id:int
    author_id: int

    class Config:
        orm_mode = True       

class Book(BaseModel):
    title:str
    author: str

    class Config:
        orm_mode = True       


class Author(BaseModel):
    name:str
    books:str

    class Config:
        orm_mode = True       


class AuthorBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class BookBase(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True

class BookSchema(BookBase):
    authors: List[AuthorBase]

class AuthorSchema(AuthorBase):
    books: List[BookBase]