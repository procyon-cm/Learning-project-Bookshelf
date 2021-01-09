from enum import unique
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.sql.schema import Table
from sqlalchemy.orm import relationship


from .database import Base

# many to many
book_author_table = Table('book_author_table', Base.metadata,
    Column('book_id', Integer, ForeignKey('book.id')),
    Column('author_id', Integer, ForeignKey('author.id'))
)

book_category_table = Table('book_category_table', Base.metadata,
    Column('book_id', Integer, ForeignKey('book.id')),
    Column('category_id', Integer, ForeignKey('category.id'))
)

class BookAuthor(Base):
    __tablename__ = "book_author_table"
    __table_args__ = {'extend_existing': True}
    
    book_id = Column(Integer, ForeignKey('book.id'), primary_key=True)
    author_id = Column(Integer, ForeignKey('author.id'), primary_key=True)

class BookCategory(Base):
    __tablename__ = "book_category_table"
    __table_args__ = {'extend_existing': True}
    
    book_id = Column(Integer, ForeignKey('book.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'), primary_key=True)    

class Book(Base):
    __tablename__ = "book"
    
    id = Column(String, primary_key=True)
    title = Column(String)
    publisher_id = Column(Integer, ForeignKey("publisher.id"))
    publishedDate = Column(String)
    pageCount = Column(Integer)
    print_type_id = Column(Integer, ForeignKey("print_type.id"))
    averageRating = Column(Float)
    ratingsCount = Column(Integer)
    language_id = Column(Integer, ForeignKey("language.id"))
    # is_read = Column(Boolean, default=False)

    authors = relationship("Author", secondary=book_author_table, back_populates="books")
    categories = relationship("Category", secondary=book_category_table, back_populates="books")
    publisher = relationship("Publisher", back_populates="books")
    print_type = relationship("PrintType", back_populates="books")
    language = relationship("Language", back_populates="books")
    industry_identifiers = relationship("IndustryIdentifier", back_populates="book")

class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)
    
    books = relationship("Book", secondary=book_author_table, back_populates="authors")


class Publisher(Base):
    __tablename__ = "publisher"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)

    books = relationship("Book", back_populates="publisher")

class PrintType(Base):
    __tablename__ = "print_type"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)

    books = relationship("Book", back_populates="print_type")

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)

    books = relationship("Book", secondary=book_category_table, back_populates="categories")

class Language(Base):
    __tablename__ = "language"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)

    books = relationship("Book", back_populates="language")

class IndustryIdentifier(Base):
    __tablename__ = "industry_identifier"
    id = Column(String, primary_key=True, unique=True, nullable=False)
    name = Column(String, ForeignKey("identifier_type.id"))
    book_id = Column(String, ForeignKey("book.id"))
    
    book = relationship("Book", back_populates="industry_identifiers")
    type = relationship("IdentifierType")

class IdentifierType(Base):
    __tablename__ = "identifier_type"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String, unique=True)

