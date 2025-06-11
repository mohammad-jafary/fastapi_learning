from fastapi import Body, FastAPI, HTTPException

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


# Just a simple api-endpoint
@app.get("/api-endpoint")
async def first_api():
    return {'message': 'Hello World!'}


# Giving the title via ?title= | httpexception error
@app.get("/books/")
async def read_all_books(title: str):
    for book in BOOKS:
        db_title = book.get('title')
        if db_title and db_title.casefold() == title.casefold():
            return book
    raise HTTPException(
        status_code=404,
        detail=f"Book with title {title} was not found!"
    )


# Giving the author and category one with url parameter another via ?=
@app.get("/book/{book_author}/")
async def read_books_by_author(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
                book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

    raise HTTPException(
        status_code=404,
        detail="Not Found"
    )


# first and most simple post message. post has body and get does not.
@app.post("/book/create_book")
async def create_new_book(new_book=Body()):
    BOOKS.append(new_book)


