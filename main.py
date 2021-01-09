
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
import requests
from sql_app import crud
from sql_app import api_models

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

@app.get("/v1/books/internal/{book_id}")
def saved_book_by_id(book_id: str, db: Session = Depends(get_db)):
    db_book = get_saved_book_by_id(db, id=book_id)
    print(db_book)
    if db_book is None: 
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.get("/v1/books/internal")
def get_book_from_database(title: str, author: Optional[str] = None, category: Optional[str] = None, db: Session = Depends(get_db)):
    
    db_book = get_saved_books(title = title, author = author, category = category, db=db)
    if db_book is None or (title == None and author == None and category == None):
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.post("/v1/books/internal")
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):     
    crud.create_book(db=db, book=book)


@app.get("/v1/books/external")
def get_book(key_words: str, subject: Optional[str] = None, author: Optional[str] = None):

    
    value = "intitle:" + key_words
    if subject:
        value += " subject:" + subject
    if author:
        value += " inauthor:" + author
     
    payload = { "q": value }
    r = requests.get("https://www.googleapis.com/books/v1/volumes", params=payload)
    book = Books.parse_raw(r.text)
    return(book)


@app.get("/v1/books/external/{book_id}")
def get_book_by_id(book_id: str):
    url = "https://www.googleapis.com/books/v1/volumes/" + book_id
    r = requests.get(url)
    book = Book.parse_raw(r.text)
    return(book)



