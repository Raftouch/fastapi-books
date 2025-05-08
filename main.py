from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Annotated


app = FastAPI()

engine = create_async_engine("sqlite+aiosqlite:///books.db")

new_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

class BookDB(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]

class BookCreateSchema(BaseModel):
    title: str
    author: str

class BookSchema(BookCreateSchema):
    id: int

    
async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


@app.post("/setup_db", tags=["Setup DB 📁"])
async def setup_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    return {"success": True}


@app.post("/books", tags=["Books 📚"], summary='Add a book')
async def add_book(data: BookCreateSchema, session: SessionDep):
    new_book = BookDB(
        title=data.title, 
        author=data.author
    )
    session.add(new_book)
    await session.commit()
    return {"success": True, "message": "Book has been added"}


@app.get("/books", tags=["Books 📚"], summary='Get all books')
async def get_all_books(session: SessionDep):
    query = select(BookDB)
    result = await session.execute(query)
    return result.scalars().all()


@app.get("/books/{id}", tags=["Books 📚"], summary='Get one book')
async def get_book(id: int, session: SessionDep):
    query = select(BookDB).filter(BookDB.id == id)
    result = await session.execute(query)
    book = result.scalar_one_or_none()

    if book is None:
        raise HTTPException(status_code=404, detail=f"No book found for id {id}")
    
    return book


@app.delete("/books/{id}", tags=["Books 📚"], summary="Delete a book")
async def remove_book(id: int, session: SessionDep):
    query = select(BookDB).filter(BookDB.id == id)
    result = await session.execute(query)
    book = result.scalar_one_or_none()

    if book is None:
        raise HTTPException(status_code=404, detail=f"No book found for id {id}")
    
    await session.delete(book)
    await session.commit()

    return {"success": True, "message": "Book has been removed"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)