from typing import Optional
from sqlalchemy.orm import Session

from sql_app import models, schemas

def get_book(db: Session, key_words: str, category: Optional[str] = None, author: Optional[str] = None):
    search = "%{}%".format(key_words)
    books = db.query.filter(models.Book.title.like(search)).limit(10).all()
 
    return books

def get_book_by_id(db: Session, id: str):
    return db.query(models.Book).filter(models.Book.id == id).one()

def get_book_by_title(db: Session, title: str):
    return db.query(models.Book).filter(models.Book.title == title).first()

def get_book_by_author_name(db: Session, name: str):
    return db.query(models.Book).filter(models.Author.name == name).limit(10).all() # should return multiple books

def get_book_by_category(db: Session, category: str):
    return db.query(models.Book).filter(models.Category.name == category).limit(10).all() # should return multiple books

# def get_read_books(db: Session, is_read: bool):
#     return db.query(models.Book).filter


def create_author(author_name: str):
    return models.Author(name = author_name)

def create_publisher(publisher_name: str):
    return models.Publisher(name = publisher_name)

def create_print_type(print_type_name: str):
    return models.PrintType(name = print_type_name)
   
def create_category(category_name: str):
    return models.Category(name = category_name)

def create_language(language_name: str):
    return models.Language(name = language_name)

def create_identifier_type(identifier_type_name: str):
    return models.IdentifierType(name = identifier_type_name)

def create_industry_identifier(industry_identifier_name: str, identifier_type: models.IdentifierType):
    return models.IndustryIdentifier(name = industry_identifier_name, type = identifier_type)

def create_industry_identifier_with_type(identifier_type_name, industry_identifier_name):
    type = create_identifier_type(identifier_type_name)
    return create_industry_identifier(industry_identifier_name, type)

def create_book(db: Session, book: schemas.BookCreate):

    foreign_id_dict = dict()    

    stored_authors = map(lambda author: create_author(author), book.volumeInfo.authors)
    foreign_id_dict["authors"] = list(stored_authors)

    if book.volumeInfo.categories is not None:
        stored_categories = map(lambda category: create_category(category), book.volumeInfo.categories)
        foreign_id_dict["categories"] = list(stored_categories)

    if book.volumeInfo.publisher is not None:
        stored_publisher = create_publisher(book.volumeInfo.publisher)
        foreign_id_dict["publisher"] = stored_publisher

    if book.volumeInfo.printType is not None:
        stored_print_type = create_print_type(book.volumeInfo.printType)
        # if db.query(models.Book).filter(models.Book.print_type == stored_print_type).first() is None:
        foreign_id_dict["print_type"] = stored_print_type
            
    if book.volumeInfo.language is not None:
        stored_language = create_language(book.volumeInfo.language)
        # if db.query(models.Book).filter(models.Book.language == stored_language).first() is None:
        foreign_id_dict["language"] = stored_language
      
    if book.volumeInfo.industryIdentifiers is not None:
        stored_industry_identifiers = map(lambda industry_identifier: create_industry_identifier_with_type(industry_identifier.type, industry_identifier.identifier), book.volumeInfo.industryIdentifiers)
        foreign_id_dict["industry_identifiers"] = list(stored_industry_identifiers)



    new_book = dict()
    new_book["id"] = book.id
    new_book["title"] = book.volumeInfo.title
    new_book["publishedDate"] = book.volumeInfo.publishedDate
    new_book["pageCount"] = book.volumeInfo.pageCount
    new_book["averageRating"] = book.volumeInfo.averageRating
    new_book["ratingsCount"] = book.volumeInfo.ratingsCount
   
   

    new_book.update(foreign_id_dict)

    print(new_book)

    db_book = models.Book(**new_book)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book