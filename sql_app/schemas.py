from typing import List, Optional

from pydantic import BaseModel


class IndustryIdentifiers(BaseModel):
    type: str
    identifier: str


class VolumeInfo(BaseModel):
    title: str 
    authors: List[str]
    publisher: Optional[str]
    publishedDate: Optional[str]
    industryIdentifiers: Optional[List[IndustryIdentifiers]]
    pageCount: Optional[int]
    printType: Optional[str]
    categories: Optional[List[str]]
    averageRating: Optional[float]
    ratingsCount: Optional[int]
    language: Optional[str]

class BookBase(BaseModel):
    id: str
    volumeInfo: VolumeInfo = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    # is_read: bool

    class Config:
        orm_mode = True

class Books(BaseModel):
    items: List[Book]
