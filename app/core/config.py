from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict
from app.schemas.file import FileType
from app.schemas.configs import StorageAdapterConfig


class Settings(BaseSettings):
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

    # S3
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str

    S3_INVOICE_ACCESS_KEY: str
    S3_INVOICE_SECRET_KEY: str

    S3_PDF_HOST: str
    S3_IMAGE_HOST: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    def storage_adapters(self) -> Dict[FileType, StorageAdapterConfig]:
        return {
            FileType.PDF_CO: StorageAdapterConfig(
                type="s3",
                config={
                    "pub_bucket_url": self.S3_PDF_HOST,
                    "bucket_name": "orders-pdf-bucket",
                    "region": "eu-central-1",
                    "access_key": self.S3_ACCESS_KEY,
                    "secret_key": self.S3_SECRET_KEY,
                },
            ),
            FileType.PDF_INVOICE: StorageAdapterConfig(
                type="s3",
                config={
                    "pub_bucket_url": self.S3_PDF_HOST,
                    "bucket_name": "orders-pdf-bucket",
                    "region": "eu-central-1",
                    "access_key": self.S3_INVOICE_ACCESS_KEY,
                    "secret_key": self.S3_INVOICE_SECRET_KEY,
                },
            ),
            FileType.PDF_SPEC: StorageAdapterConfig(
                type="s3",
                config={
                    "pub_bucket_url": self.S3_PDF_HOST,
                    "bucket_name": "orders-pdf-bucket",
                    "region": "eu-central-1",
                    "access_key": self.S3_INVOICE_ACCESS_KEY,
                    "secret_key": self.S3_INVOICE_SECRET_KEY,
                },
            ),
            FileType.PRODUCT_IMAGE: StorageAdapterConfig(
                type="s3",
                config={
                    "pub_bucket_url": self.S3_IMAGE_HOST,
                    "bucket_name": "orders-pdf-bucket",
                    "region": "eu-central-1",
                    "access_key": self.S3_INVOICE_ACCESS_KEY,
                    "secret_key": self.S3_INVOICE_SECRET_KEY,
                },
            ),
        }


settings = Settings()

        # FileType.IMAGE_STORAGE: StorageAdapterConfig(
        #     type="s3",
        #     config={
        #         "bucket_name": "gwm-image-bucket",
        #         "project_id": "my-gcp-project",
        #         "credentials_file": os.getenv("GWM_CREDENTIALS"),
        #     },
        # ),
        # FileType.LOCAL_STORAGE: StorageAdapterConfig(
        #     type="s3",
        #     config={
        #         "storage_path": "/var/storage/files",
        #         "host": "127.0.0.1",
        #         "port": 9000,
        #     },
        # )
    # }


