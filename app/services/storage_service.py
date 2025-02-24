from typing import Dict, Optional, Type
from sqlalchemy.orm import Session
from app.adapters.s3_adapter import S3Adapter
from app.adapters.tcp_adapter import TCPAdapter
from app.adapters.gwm_adapter import GWMAdapter
from app.adapters.base import BaseStorageAdapter
from app.core.config import settings
from app.schemas.file import FileType
import os


class StorageService:
    # Маппинг доступных адаптеров
    ADAPTERS: Dict[str, Type[BaseStorageAdapter]] = {
        "s3": S3Adapter,
        "tcp": TCPAdapter,
        "gwm": GWMAdapter,
    }

    def __init__(self):
        self.adapters: Dict[FileType, BaseStorageAdapter] = {}

        # Инициализация адаптеров по конфигурации
        for file_type, adapter_data in settings.storage_adapters.items():
            adapter_type = adapter_data.type
            config = adapter_data.config

            # Проверяем, есть ли адаптер в маппинге
            adapter_class = self.ADAPTERS.get(adapter_type)
            if not adapter_class:
                raise ValueError(f"Неизвестный адаптер хранения: {adapter_type}")

            # Создаем экземпляр адаптера
            self.adapters[file_type] = adapter_class(config)

    def upload_file(self, db: Session, file_type: FileType, file_path: str, file_name: str, folder: Optional[str] = None, tags: Optional[list] = None):
        if file_type not in self.adapters:
            raise ValueError(f"Адаптер для типа '{file_type}' не настроен")

        adapter = self.adapters[file_type]
        result = adapter.upload_file(file_path, file_name, folder)

        file_id = result["file_id"]
        file_url = result["url"]
        file_size = os.path.getsize(file_path)
        file_extension = os.path.splitext(file_name)[-1].lstrip(".")

        return {"file_id": file_id, "url": file_url, "file_size":file_size, "file_extension":file_extension}

