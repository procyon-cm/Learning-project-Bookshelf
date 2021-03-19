
from fastapi import FastAPI
from fastapi import Depends, HTTPException
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

# Get one book from the internal database by its ID
@app.get("/v1/books/internal/{book_id}")
def saved_book_by_id(book_id: str, db: Session = Depends(get_db)):
    db_book = get_saved_book_by_id(db, id=book_id)
    if db_book is None: 
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

# Get list of all books stored in the internal database
@app.get("/v1/books/all")
def get_list_of_all_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = get_all_books(db, skip=skip, limit=limit)  
    return books


# Get books from internal database by request parameters
@app.get("/v1/books/internal")
def get_book_from_database(title: str, author: Optional[str] = None, category: Optional[str] = None, is_read: Optional[bool] = None, db: Session = Depends(get_db)):
    
    db_book = get_saved_books(is_read = is_read, title = title, author = author, category = category, db = db)
    if db_book is None or (title == None and author == None and category == None and is_read == None):
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

# Save book into the internal database
@app.post("/v1/books/internal")
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):     
    crud.create_book(db=db, book=book)
    return "Book successfully stored to database."

@app.delete("/v1/books/{book_id}")
def delete_book(book_id: str, db: Session = Depends(get_db)):
    db_book = delete_book_by_id(db, id=book_id)
    if db_book is None: 
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

# Get books from Google Books API by request parameters
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

# Get one book from Google Books API by its ID
@app.get("/v1/books/external/{book_id}")
def get_book_by_id(book_id: str):
    url = "https://www.googleapis.com/books/v1/volumes/" + book_id
    r = requests.get(url)
    book = Book.parse_raw(r.text)
    return(book)



