from abc import ABC, abstractmethod
from typing import Dict, Optional


class BaseStorageAdapter(ABC):
    def __init__(self, config: Dict):
        """
        Базовый класс для всех адаптеров хранения.
        :param config: Словарь с конфигурацией адаптера
        """
        self.config = config

    @abstractmethod
    def upload_file(self, file_path: str, file_name: str, folder: Optional[str] = None) -> Dict[str, str]:
        """
        Абстрактный метод для загрузки файлов.
        :param file_path: Путь к файлу на сервере
        :param file_name: Имя файла
        :param folder: Каталог (префикс) внутри хранилища
        :return: Словарь с file_id и url
        """
        pass
