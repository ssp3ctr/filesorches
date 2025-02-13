import os
import shutil
from app.adapters.base import BaseStorageAdapter
from typing import Dict

class TCPAdapter(BaseStorageAdapter):
    def __init__(self, config: Dict):
        super().__init__(config)
        self.storage_path = config["storage_path"]
        self.host = config["host"]
        self.port = config["port"]

        # Создаем папку, если ее нет
        os.makedirs(self.storage_path, exist_ok=True)

    def upload_file(self, file_path: str, file_name: str) -> Dict[str, str]:
        dest_path = os.path.join(self.storage_path, file_name)

        try:
            shutil.move(file_path, dest_path)
            file_url = f"tcp://{self.host}:{self.port}/{file_name}"
            return {"file_id": file_name, "url": file_url}
        except Exception as e:
            raise Exception(f"Ошибка при сохранении файла: {str(e)}")
