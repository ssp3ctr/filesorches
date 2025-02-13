import boto3
from botocore.exceptions import NoCredentialsError, BotoCoreError
from app.adapters.base import BaseStorageAdapter
from typing import Dict, Optional

class S3Adapter(BaseStorageAdapter):
    def __init__(self, config: Dict):
        super().__init__(config)
        self.bucket_name = config["bucket_name"]
        self.region = config["region"]
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=config["access_key"],
            aws_secret_access_key=config["secret_key"],
            region_name=self.region,
        )

    def upload_file(self, file_path: str, file_name: str, folder: Optional[str] = None) -> Dict[str, str]:
        """
        Загружает файл в S3, поддерживает каталоги (префиксы).
        :param file_path: путь к файлу
        :param file_name: имя файла
        :param folder: подкаталог в S3 (если нужен)
        :return: словарь с file_id и url
        """
        try:
            # Если указан подкаталог, добавляем его к пути
            s3_key = f"{folder}/{file_name}" if folder else file_name

            # Загружаем файл в S3
            self.s3_client.upload_file(file_path, self.bucket_name, s3_key)

            # Формируем URL файла
            file_url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{s3_key}"

            return {"file_id": s3_key, "url": file_url}

        except NoCredentialsError:
            raise Exception("Ошибка авторизации AWS S3: Проверьте access_key и secret_key")
        except BotoCoreError as e:
            raise Exception(f"Ошибка работы с S3: {str(e)}")
