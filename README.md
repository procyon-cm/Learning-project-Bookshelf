# Learning project Bookshelf

## About
This **project Bookshelf** was created for the purpose of improving my skills as backend developer-beginner. It is written in **Python 3** and uses multiple frameworks and libraries (e.g. FastAPI, SQLalchemy, relational database SQLite etc. - more info in Technology section). The main funcionality of the Bookshelf is searching information about books via Google Books API and creating personal database with books user's interested in.

## Technology
**FastAPI framework** was used for building the web server - documentation for [FastAPI](https://github.com/tiangolo/fastapi) available on GitHub. Data returned from Google Books API are processed by **Pydantic** ([more info](https://pydantic-docs.helpmanual.io/)) and with use of **SQLAlchemy** ([more info](https://www.sqlalchemy.org/)) are stored to the relational database **SQLite**. User can search book info in the database using multiple criteria - specified in the section Examples.
## Requirements
To run this project, it's necessary to have installed frameworks mentioned above. Installation instructions are available in attached links. 
## Examples
Starting the server:
>`uvicorn main:app --reload`

Searching in Google Books database by *book-id*:
> `GET localhost:8000/v1/books/external/Xq3bDAAAQBAJ`

Searching in Google Books database by *key words* (this field is required) and optional criteria *author* and *subject*:
> `GET localhost:8000/v1/books/external?key_words=harry potter&author=rowling&subject=fiction`

Saving a book into internal database:
> `POST localhost:8000/v1/books/internal`

Loading book info from internal database (search criteria: *title* (required), *author* (optional), *category* (optional)).
> `GET localhost:8000/v1/books/internal?title=levhart&author=nesbo&category=fiction`

In file *sql_app.db* is example of created database with 20 saved books.
## Future improvements
Next steps to improve this project are addition of another searching criteria and making every one of them optional (eg. title is now requiered). Also boolean value for each saved book (already read/not read yet) would be useful.

Error handling needs to be improved as well (Google Books API responses and database errors).