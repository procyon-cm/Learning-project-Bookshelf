from typing import List, Optional
from sqlalchemy.orm import Session

from sql_app import models, schemas

def get_book(db: Session, key_words: str, category: Optional[str] = None, author: Optional[str] = None):
    search = "%{}%".format(key_words, category, author)
    books = db.query.filter(models.Book.title.like(search)).limit(10).all()
    return books

def get_book_from_db(db: Session, saved_book: models.Book):
    saved_book_dict = dict()
    saved_book_dict["id"] = saved_book.id
    saved_book_dict["title"] = saved_book.title
    
    authors_list = list(map(lambda author: author.name, saved_book.authors))
    saved_book_dict["authors"] = authors_list

    saved_book_dict["publisher"] = saved_book.publisher
    saved_book_dict["publishedDate"] = saved_book.publishedDate
    identifiers_list = list(map(lambda identifier: identifier.type.name, saved_book.industry_identifiers))
    saved_book_dict["industry_identifiers"] = identifiers_list

    saved_book_dict["pageCount"] = saved_book.pageCount
    saved_book_dict["print_type"] = saved_book.print_type.name
    
    category_list = list(map(lambda category: category.name, saved_book.categories))
    saved_book_dict["categories"] = category_list
    
    saved_book_dict["averageRating"] = saved_book.averageRating
    saved_book_dict["ratingsCount"] = saved_book.ratingsCount
    saved_book_dict["language"] = saved_book.language.name
    return saved_book_dict

def get_saved_book_by_id(db: Session, id: str):
    try:
        saved_book = db.query(models.Book).filter(models.Book.id == id).one()
        book = get_book_from_db(db, saved_book = saved_book)
        return book
    except:
        return None
        

def get_saved_books(db: Session, title: str, author: str, category: str):
    try:
        saved_books = None

        if title:
            search_title = "%{}%".format(title)
            saved_books = db.query(models.Book).filter(models.Book.title.like(search_title))

        if author != None:
            search_author = "%{}%".format(author)
            saved_books = saved_books.filter(models.Author.name.like(search_author))

        if category != None:
            search_category = "%{}%".format(category)
            saved_books = saved_books.filter(models.Category.name.like(search_category))

        books = list(map(lambda book: get_book_from_db(db, book), saved_books))
        return books 
    except:
        return None



# def get_read_books(db: Session, is_read: bool):
# return db.query(models.Book).filter


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
    return models.IndustryIdentifier(id = industry_identifier_name, type = identifier_type)

def create_industry_identifier_with_type(industry_identifier: schemas.IndustryIdentifiers):
    type = create_identifier_type(industry_identifier.type)
    return create_industry_identifier(industry_identifier.identifier, type)

def create_and_store_bookauthor(book_id: models.Book.id, author: models.Author, db: Session):
    bookauthor = models.BookAuthor(book_id = book_id, author_id = author.id)
    db.add(bookauthor)
    db.commit()
    db.refresh(bookauthor) 
    return bookauthor

def create_and_store_bookcategory(book_id: models.Book.id, category: models.Category, db: Session):
    bookcategory = models.BookCategory(book_id = book_id, category_id = category.id)
    db.add(bookcategory)
    db.commit()
    db.refresh(bookcategory) 
    return bookcategory

def create_and_store_industry_identifiers(book_id: models.Book.id, identifier_types, db: Session):
    print(identifier_types)
    for identifier_type, tup in identifier_types.items():
        db_industry_identifier = models.IndustryIdentifier(name = tup[0], book_id = book_id, id = tup[1])
        db.add(db_industry_identifier)
        db.commit()
        db.refresh(db_industry_identifier)

def create_book(db: Session, book: schemas.BookCreate):

    foreign_id_dict = dict()    

    stored_authors = list(map(lambda author: create_author(author), book.volumeInfo.authors))
    first_author_in_db = db.query(models.Author).first()
    authors = list()
    authors_in_db = list()
    industry_types_in_db = list()
    categories_in_db = list()

    if first_author_in_db == None:
        authors = stored_authors
    else:
        for author in stored_authors:
            author_in_db = db.query(models.Author).filter(models.Author.name == author.name).first()
            if author_in_db == None:
                authors.append(author)
            else:
                authors_in_db.append(author_in_db)
    foreign_id_dict["authors"] = authors
    print(foreign_id_dict)

    if book.volumeInfo.categories is not None:
        stored_categories = list(map(lambda category: create_category(category), book.volumeInfo.categories))
        categories = list()
        for category in stored_categories:
            category_in_db = db.query(models.Category).filter(models.Category.name == category.name).first()
            if category_in_db == None:
                categories.append(category)
            else: 
                categories_in_db.append(category_in_db)
            
        foreign_id_dict["categories"] = categories
    print(foreign_id_dict)

    if book.volumeInfo.publisher is not None:
        stored_publisher = create_publisher(book.volumeInfo.publisher)
        publisher_in_db = db.query(models.Publisher).filter(models.Publisher.name == stored_publisher.name).first()
        if publisher_in_db is None:
            foreign_id_dict["publisher"] = stored_publisher
        else:
            foreign_id_dict["publisher_id"] = publisher_in_db.id


    if book.volumeInfo.printType is not None:
        stored_print_type = create_print_type(book.volumeInfo.printType)
        print_type_in_db = db.query(models.PrintType).filter(models.PrintType.name == stored_print_type.name).first()
    
        if print_type_in_db is None:
            foreign_id_dict["print_type"] = stored_print_type
        else:
            foreign_id_dict["print_type_id"] = print_type_in_db.id        

            
    if book.volumeInfo.language is not None:
        stored_language = create_language(book.volumeInfo.language)
        language_in_db = db.query(models.Language).filter(models.Language.name == stored_language.name).first()
        if language_in_db is None:  
            foreign_id_dict["language"] = stored_language
        else:
            foreign_id_dict["language_id"] = language_in_db.id
    
    db_industry_identifier_types_with_values = dict()    
    if book.volumeInfo.industryIdentifiers is not None:
         
        stored_industry_identifiers = list(map(lambda industry_identifier: create_industry_identifier_with_type(industry_identifier), book.volumeInfo.industryIdentifiers))
        print(stored_industry_identifiers)
        name_of_types = list(map(lambda industry_identifier: industry_identifier.type.name, stored_industry_identifiers))
        print(name_of_types)
        industry_types_in_db = db.query(models.IdentifierType).filter(models.IdentifierType.name.in_(name_of_types)).all()
        stored_type_names = list(map(lambda stored_type: stored_type.name, industry_types_in_db))
        if industry_types_in_db is not None:
            print(stored_type_names)
            db_industry_identifier_types_with_values = dict([(type.name, (type.id, None)) for type in industry_types_in_db])
            for identifier in book.volumeInfo.industryIdentifiers:
                if identifier.type in db_industry_identifier_types_with_values:
                    db_industry_identifier_types_with_values[identifier.type] = (db_industry_identifier_types_with_values[identifier.type][0], identifier.identifier)
            stored_industry_identifiers = list(filter(lambda identifier_type: identifier_type.type.name not in stored_type_names, stored_industry_identifiers))
        print(industry_types_in_db)
        foreign_id_dict["industry_identifiers"] = stored_industry_identifiers







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

    for db_author in authors_in_db:
        create_and_store_bookauthor(db_book.id, db_author, db)

    if book.volumeInfo.categories is not None and len(categories_in_db) > 0:
        for db_category in categories_in_db:
            create_and_store_bookcategory(db_book.id, db_category, db)
        
    if industry_types_in_db is not None:
        create_and_store_industry_identifiers(db_book.id, db_industry_identifier_types_with_values, db)

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    
    
    
    
    
    return db_book