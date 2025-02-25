from abc import ABC, abstractmethod
from typing import Dict, Optional


class BaseStorageAdapter(ABC):
    def __init__(self, config: Dict):
        """
        Base class for all storage adapters.
            :param config: Dictionary with adapter configuration
        """

        self.config = config

    @abstractmethod
    def upload_file(self, file_path: str, file_name: str, folder: Optional[str] = None) -> Dict[str, str]:
        """
        Abstract method for uploading files.
            :param file_path: Path to the file on the server
            :param file_name: Name of the file
            :param folder: Directory (prefix) within the storage
            :return: Dictionary with file_id and url
        """
        pass
