from fastapi import APIRouter, Depends, HTTPException
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from src.books.schemas import CreateBookModel, BookModel


book_router = APIRouter(prefix="/books")
book_service = BookService()


@book_router.post("/", response_model=BookModel)
async def create_book(book_data: CreateBookModel, session: AsyncSession = Depends(get_session)):
    book = await book_service.create_book(book_data, session)
    if book:
        return book
    raise HTTPException(status_code=404, detail="Book not found")


@book_router.get("/", response_model=list[BookModel])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    print("Getting all books")
    return await book_service.get_all_books(session)
