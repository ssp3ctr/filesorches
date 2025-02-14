from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
import shutil
import tempfile
import os
import uuid

from app.database.postgre_engine import get_db
from app.schemas.file_type import FileType
from app.services.file_metadata_service import FileService
from app.services.storage_service import StorageService

router = APIRouter()

@router.post("/files/")
async def create_file(
    file: UploadFile = File(...),
    file_type: FileType = Form(...),
    folder: Optional[str] = Form(None),
    tags: Optional[List[str]] = Form(None),
    db: Session = Depends(get_db),
):
    temp_file_path = None

    try:
        # 1. Создаём временный файл (delete=False, чтобы файл не удалился сразу после закрытия)
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            temp_file_path = tmp.name
            # Скопируем содержимое UploadFile во временный файл
            shutil.copyfileobj(file.file, tmp)

        # 2. Инициализируем сервис для загрузки (использует нужный адаптер по file_type)
        storage_service = StorageService()

        # 3. Загружаем во внешнее хранилище
        upload_result = storage_service.upload_file(
            db=db,
            file_type=file_type,
            file_path=temp_file_path,
            file_name=file.filename,
            folder=folder,
            tags=tags
        )

        # 4. Сохраняем метаданные в БД
        created_file = FileService.create_file(
            db=db,
            filename=file.filename,
            file_type=file_type,
            extension=upload_result["file_extension"],
            size=upload_result["file_size"],
            tags=tags or []
        )

        return {
            "status": "success",
            "file_id": upload_result["file_id"],  # ID файла в системе хранения
            "url": upload_result["url"],          # URL файла в хранилище
            "db_id": created_file.id,             # ID записи в базе
        }

    finally:
        # 5. Удаляем временный файл в любом случае (даже если выше возникла ошибка)
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@router.get("/files/{file_id}")
def get_file(file_id: uuid.UUID, db: Session = Depends(get_db)):
    file = FileService.get_file_by_id(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="Файл не найден")
    return file

@router.get("/files/")
def search_files_by_tags(tags: List[str], db: Session = Depends(get_db)):
    return FileService.get_files_by_tags(db, tags)

@router.delete("/files/{file_id}")
def delete_file(file_id: uuid.UUID, db: Session = Depends(get_db)):
    success = FileService.delete_file(db, file_id)
    if not success:
        raise HTTPException(status_code=404, detail="Файл не найден")
    return {"detail": "Файл удален"}

@router.put("/files/{file_id}/tags")
def update_file_tags(file_id: uuid.UUID, new_tags: List[str], db: Session = Depends(get_db)):
    file = FileService.update_file_tags(db, file_id, new_tags)
    if not file:
        raise HTTPException(status_code=404, detail="Файл не найден")
    return file
