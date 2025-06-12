from typing import Optional

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()


# A class for books
class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    publish_date: int

    def __init__(self, id, title, author, description, rating, publish_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publish_date = publish_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="Id is not needed", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    publish_date: int = Field(gt=1800, lt=2025)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "some author",
                "description": "some description",
                "rating": 5,
                "publish_date": 2012 
            }}}


BOOKS = [
    Book(1, 'MLops', 'Mohammad', 'ML somehow', 5, 2023),
    Book(2, 'ML no ops', 'Sadoughi', 'ML somehow', 4, 2023),
    Book(3, 'deep learning', 'rouhani', 'deep learning somehow', 3, 2024),
    Book(4, 'computer vision', 'fazl', 'vision somehow', 2, 2024),
    Book(5, 'image processing', 'taher', 'processing somehow', 2, 2024),
    Book(6, 'advanced image processing', 'saadatmand', 'advanced somehow', 1, 2023)
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/publish/")
async def read_book_by_publish_date(publish_date: int = Query(gt=1800, lt=2025)):
    books_to_return = []
    for book in BOOKS:
        if book.publish_date == publish_date:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(
        status_code=404,
        detail="Did not find the requested book!"
    )


@app.get("/books/")
async def read_book_by_rating(book_rating: int = Query(gt=-1, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return {"message": f"Book added successfully with id of {BOOKS[-1].id}"}


@app.put("/books/update_book")
async def update_book(book: BookRequest):
    book_updated = False
    book_to_update = Book(**book.model_dump())
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book_to_update
            book_updated = True
    if not book_updated:
        raise HTTPException(
            status_code=404,
            detail="did not find the book"
        )


@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    book_removed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_removed = True
            break
    if not book_removed:
        raise HTTPException(
            status_code=404,
            detail="Not found!"
        )


def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book
