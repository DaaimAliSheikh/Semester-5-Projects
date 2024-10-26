from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession  
from sqlalchemy.orm import sessionmaker 

engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        echo=True     # to log SQL statements
    )
)


async def init_db():
    async with engine.begin() as conn:
        # runs the code in the file, which defines models classes
        import src.db.models  # type: ignore
        await conn.run_sync(SQLModel.metadata.create_all)



async def get_session() -> AsyncSession:# type: ignore
    Session = sessionmaker( bind=engine, class_=AsyncSession, expire_on_commit=False) # type: ignore
    async with Session() as session: # type: ignore
        yield session # type: ignore
    
