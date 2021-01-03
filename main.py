
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
import requests
from sql_app import crud

from sql_app.crud import *
from sql_app.models import *
from sql_app.schemas import *
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/v1/books/internal/{id}", response_model=schemas.Book)
def read_book_by_id(id: str, db: Session = Depends(get_db)):
    db_book = get_book_by_id(db, id=id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.get("/v1/books/internal/{title}", response_model=schemas.Book)
def read_book_by_text(key_words: str, subject: Optional[str] = None, author: Optional[str] = None, db: Session = Depends(get_db)):
    db_book = get_book_by_title(db, )
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.get("/v1/books/internal/{name}", response_model=schemas.Book)
def read_book_by_author_name(name: str, db: Session = Depends(get_db)):
    db_book = get_book_by_author_name(db, name=name)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.get("/v1/books/internal/{category}", response_model=schemas.Book)
def read_book_by_category(category: str, db: Session = Depends(get_db)):
    db_book = get_book_by_category(db, category=category)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.post("/v1/books/internal", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/v1/books/external")
def get_book(key_words: str, subject: Optional[str] = None, author: Optional[str] = None):
    # print(key_words, subject, author)
    
    value = "intitle:" + key_words
    if subject:
        value += " subject:" + subject
    if author:
        value += " inauthor:" + author
     
    payload = { "q": value }
    # print(payload)
    r = requests.get("https://www.googleapis.com/books/v1/volumes", params=payload)
    # print(r.url)
    book = Books.parse_raw(r.text)
    return(book)


@app.get("/v1/books/external/{book_id}")
def get_book_by_id(book_id: str):
    url = "https://www.googleapis.com/books/v1/volumes/" + book_id
    # print(url)
    r = requests.get(url)
    book = Book.parse_raw(r.text)
    return(book)



