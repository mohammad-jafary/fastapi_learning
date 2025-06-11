from fastapi import FastAPI

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


BOOKS = [
    Book(1, 'MLops', 'Mohammad', 'ML somehow', 5),
    Book(2, 'ML no ops', 'Sadoughi', 'ML somehow', 4),
    Book(3, 'deep learning', 'rouhani', 'deep learning somehow', 3),
    Book(4, 'computer vision', 'fazl', 'vision somehow', 2),
    Book(5, 'image processing', 'taher', 'processing somehow', 2),
    Book(6, 'advanced image processing', 'saadatmand', 'advanced somehow', 1)
]


@app.get("/books")
async def read_all_books():
    return BOOKS
