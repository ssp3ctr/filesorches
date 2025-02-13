from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.postgre_engine import SessionLocal
from app.services.file_metadata_service import FileService
from app.schemas.file_type import FileType
import uuid
from typing import List

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/files/")
def create_file(
    filename: str,
    file_type: FileType,
    extension: str,
    size: int,
    tags: List[str],
    db: Session = Depends(get_db),
):
    return FileService.create_file(db, filename, file_type, extension, size, tags)

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
