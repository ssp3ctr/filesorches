from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
import shutil
import tempfile
import os
import uuid

from app.database.postgre_engine import get_db
from app.schemas.file import FileType
from app.services.file_metadata_service import FileMetadataService
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
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            temp_file_path = tmp.name
            shutil.copyfileobj(file.file, tmp)

        storage_service = StorageService()

        upload_result = storage_service.upload_file(
            db=db,
            file_type=file_type,
            file_path=temp_file_path,
            file_name=file.filename,
            folder=folder,
            tags=tags
        )

        created_file = FileMetadataService.create_file(
            db=db,
            filename=file.filename,
            file_type=file_type,
            filepath=upload_result["url"],
            extension=upload_result["file_extension"],
            size=upload_result["file_size"],
            tags=tags or []
        )

        return {
            "status": "success",
            "file_id": upload_result["file_id"],
            "url": upload_result["url"],
            "db_id": created_file.id,
        }

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@router.get("/files/{file_id}")
def get_file(file_id: uuid.UUID, db: Session = Depends(get_db)):
    file = FileMetadataService.get_file_by_id(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="Файл не найден")
    return file


@router.get("/files/")
def search_files_by_tags(
    tags: List[str] = Query(..., description="List of tags"),
    db: Session = Depends(get_db)
):
    return FileMetadataService.get_files_by_tags(db, tags)


@router.delete("/files/{file_id}")
def delete_file(file_id: uuid.UUID, db: Session = Depends(get_db)):
    success = FileMetadataService.delete_file(db, file_id)
    if not success:
        raise HTTPException(status_code=404, detail="Файл не найден")
    return {"detail": "Файл удален"}


@router.put("/files/{file_id}/tags")
def update_file_tags(file_id: uuid.UUID, new_tags: List[str], db: Session = Depends(get_db)):
    file = FileMetadataService.update_file_tags(db, file_id, new_tags)
    if not file:
        raise HTTPException(status_code=404, detail="Файл не найден")
    return file
