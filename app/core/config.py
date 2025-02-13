from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, Literal, Any
from app.schemas.file_type import FileType
import os

class StorageAdapterConfig(BaseModel):
    type: Literal["s3", "gwm", "tcp"]
    config: Dict[str, Any]

class Settings(BaseSettings):
    # Use the new-style model_config instead of class Config
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
    )

    # Keycloak
    KEYCLOAK_URL: str
    KEYCLOAK_REALM: str
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_CLIENT_SECRET: str

    # PostgreSQL
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Маппинг типов файлов на адаптеры
    STORAGE_ADAPTERS: Dict[FileType, StorageAdapterConfig] = {
        FileType.PDF_CO: StorageAdapterConfig(
            type="s3",
            config={
                "bucket_name": "pdf-co-bucket",
                "region": "us-west-1",
                "access_key": os.getenv("S3_ACCESS_KEY"),
                "secret_key": os.getenv("S3_SECRET_KEY"),
            },
        ),
        FileType.PDF_INVOICE: StorageAdapterConfig(
            type="s3",
            config={
                "bucket_name": "pdf-invoice-bucket",
                "region": "eu-central-1",
                "access_key": os.getenv("S3_INVOICE_ACCESS_KEY"),
                "secret_key": os.getenv("S3_INVOICE_SECRET_KEY"),
            },
        ),
        FileType.IMAGE_STORAGE: StorageAdapterConfig(
            type="gwm",
            config={
                "bucket_name": "gwm-image-bucket",
                "project_id": "my-gcp-project",
                "credentials_file": os.getenv("GWM_CREDENTIALS"),
            },
        ),
        FileType.LOCAL_STORAGE: StorageAdapterConfig(
            type="tcp",
            config={
                "storage_path": "/var/storage/files",
                "host": "127.0.0.1",
                "port": 9000,
            },
        ),
    }

settings = Settings()
