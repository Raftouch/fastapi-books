from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel

app = FastAPI()

books = [
    {"id": 1, "title": "The Midnight Library", "author": "Matt Haig"},
    {"id": 2, "title": "Project Hail Mary", "author": "Andy Weir"},
    {"id": 3, "title": "The Song of Achilles", "author": "Madeline Miller"},
    {"id": 4, "title": "Klara and the Sun", "author": "Kazuo Ishiguro"}
]


@app.get("/", tags=["Books 📚"], summary='Get all books')
def get_all_books():
    return books


@app.get("/{id}", tags=["Books 📚"], summary='Get one book')
def get_book(id: int):
    for book in books:
        if book["id"] == id:
            return book
    raise HTTPException(status_code=404, detail=f"No book found for id {id}")


class Book(BaseModel):
    title: str
    author: str


@app.post("/", tags=["Books 📚"], summary='Add a book')
def add_book(new_book: Book):
    book_to_add = {"id": len(books) + 1, "title": new_book.title, "author": new_book.author}
    books.append(book_to_add)
    return {"success": True, "message": "Book has been added"}


@app.delete("/{id}", tags=["Books 📚"], summary="Delete a book")
def remove_book(id: int):
    for book in books:
        if book["id"] == id:
            books.remove(book)
            return {"success": True, "message": "Book has been removed"}
    raise HTTPException(status_code=404, detail=f"No book found for id {id}")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)