import uuid
from sqlalchemy import Column, String, Integer, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, UTC
from app.database.postgre_engine import Base


class FileMetadata(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    extension = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    tags = Column(ARRAY(String), default=[])
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

