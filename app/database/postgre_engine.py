from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Создаем асинхронный движок SQLAlchemy
engine = create_async_engine(settings.database_url, echo=True, future=True)


AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()

# Асинхронная зависимость для получения сессии
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        except Exception as e:
            await db.rollback()
            raise
        finally:
            await db.close()
