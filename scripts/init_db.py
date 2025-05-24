import asyncio
from vpnsellbot.db.models import Base
from sqlalchemy.ext.asyncio import create_async_engine

# Загрузите URL базы данных из переменных окружения
from vpnsellbot.config import DATABASE_URL

async def init_db():
    engine = create_async_engine(DATABASE_URL)

    async with engine.begin() as conn:
        # Создание всех таблиц
        await conn.run_sync(Base.metadata.create_all)

    print("База данных успешно инициализирована.")

if __name__ == "__main__":
    asyncio.run(init_db())
