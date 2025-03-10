import logging
import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from app.models.file import FileMetadata
from app.schemas.file import FileType
from datetime import datetime, UTC


class FileMetadataService:
    @staticmethod
    async def create_file(
        db: AsyncSession,
        filename: str,
        filepath: str,
        file_type: FileType,
        extension: str,
        size: int,
        tags: List[str]
    ) -> Optional[FileMetadata]:
        """ Создание записи о файле """
        db_file = FileMetadata(
            id=uuid.uuid4(),
            filename=filename,
            filetype=file_type.value,
            filepath=filepath,
            extension=extension,
            size=size,
            tags=tags,
            created_at=datetime.now(UTC).replace(tzinfo=None)
        )
        db.add(db_file)
        try:
            await db.commit()
            await db.refresh(db_file)
            return db_file
        except SQLAlchemyError as e:
            await db.rollback()
            logging.error(f"Ошибка при сохранении файла в БД: {str(e)}")
            return None

    @staticmethod
    async def get_file_by_id(db: AsyncSession, file_id: uuid.UUID) -> Optional[FileMetadata]:
        """ Получение файла по ID """
        result = await db.execute(select(FileMetadata).filter(FileMetadata.id == file_id))
        return result.scalars().first()

    @staticmethod
    async def get_files_by_tags(db: AsyncSession, tags: List[str]):
        logging.info(f"Searching for tags: {tags} (Type: {type(tags)})")

        if not isinstance(tags, list):
            raise ValueError(f"Expected list[str], but got {type(tags)}: {tags}")

        stmt = select(FileMetadata).where(FileMetadata.tags.overlap(tags))
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def delete_file(db: AsyncSession, file_id: uuid.UUID) -> bool:
        """ Удаление файла по ID """
        result = await db.execute(select(FileMetadata).filter(FileMetadata.id == file_id))
        file = result.scalars().first()
        if file:
            await db.delete(file)
            await db.commit()
            return True
        return False

    @staticmethod
    async def update_file_tags(db: AsyncSession, file_id: uuid.UUID, new_tags: List[str]) -> Optional[FileMetadata]:
        """ Обновление тегов у файла """
        result = await db.execute(select(FileMetadata).filter(FileMetadata.id == file_id))
        file = result.scalars().first()
        if file:
            file.tags = new_tags
            await db.commit()
            await db.refresh(file)
            return file
        return None
