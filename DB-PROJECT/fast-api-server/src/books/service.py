from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Book
from src.books.schemas import CreateBookModel


class BookService:
    async def get_all_books(self, session: AsyncSession):
        s = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(s)
        return result.all()

    async def create_book(
        self, book_data: CreateBookModel, session: AsyncSession
    ):
        new_book = Book(**book_data.model_dump())
        session.add(new_book)
        # transaction, so can perform multiple actions, and commit all at once
        await session.commit()
        return new_book
