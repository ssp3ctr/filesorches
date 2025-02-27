import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from app.models.file import FileMetadata
from app.schemas.file import FileType
import uuid
from typing import List, Optional


class FileMetadataService:
    @staticmethod
    def create_file(db: Session, filename: str, filepath: str, file_type: FileType, extension: str, size: int,
                    tags: List[str]) -> FileMetadata:
        """ Создание записи о файле """
        db_file = FileMetadata(
            id=uuid.uuid4(),
            filename=filename,
            filetype=file_type.value,
            filepath=filepath,
            extension=extension,
            size=size,
            tags=tags
        )
        db.add(db_file)
        try:
            db.commit()
            db.refresh(db_file)
            return db_file
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Ошибка при сохранении файла в БД: {str(e)}")

    @staticmethod
    def get_file_by_id(db: Session, file_id: uuid.UUID) -> Optional[FileMetadata]:
        """ Получение файла по ID """
        return db.query(FileMetadata).filter(FileMetadata.id == file_id).first()

    @staticmethod
    def get_files_by_tags(db: Session, tags: list[str]):
        logging.info(f"Searching for tags: {tags} (Type: {type(tags)})")

        # Убедимся, что tags - это список, а не строка
        if not isinstance(tags, list):
            raise ValueError(f"Expected list[str], but got {type(tags)}: {tags}")

        stmt = select(FileMetadata).where(FileMetadata.tags.overlap(tags))
        return db.execute(stmt).scalars().all()

    @staticmethod
    def delete_file(db: Session, file_id: uuid.UUID) -> bool:
        """ Удаление файла по ID """
        file = db.query(FileMetadata).filter(FileMetadata.id == file_id).first()
        if file:
            db.delete(file)
            db.commit()
            return True
        return False

    @staticmethod
    def update_file_tags(db: Session, file_id: uuid.UUID, new_tags: List[str]) -> Optional[FileMetadata]:
        """ Обновление тегов у файла """
        file = db.query(FileMetadata).filter(FileMetadata.id == file_id).first()
        if file:
            file.tags = new_tags
            db.commit()
            db.refresh(file)
            return file
        return None
