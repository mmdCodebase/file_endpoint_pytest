from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship
from pydantic import BaseModel, UUID4, PositiveInt, constr, validator
from db.database import Base
from typing import Optional

# SQLAlchemy model
class File(Base):
    __tablename__ = "files"
    __table_args__ = {'schema': 'OceanBridge.t8', 'extend_existing': True}

    file_id = Column(UNIQUEIDENTIFIER, primary_key=True)
    file_upload_pending = Column(Boolean, default=True)
    file_privacy_type_choice = Column(UNIQUEIDENTIFIER)
    file_is_linked_to_table = Column(String(64))
    file_is_linked_to_id = Column(UNIQUEIDENTIFIER)
    file_type_choice = Column(UNIQUEIDENTIFIER)
    file_sub_type_choice = Column(UNIQUEIDENTIFIER)
    file_size_kb = Column(Integer)
    file_name = Column(String(255))
    file_owner_entity_id = Column(UNIQUEIDENTIFIER)
    file_uploaded_by_id = Column(UNIQUEIDENTIFIER)
    file_uploaded_on = Column(DateTime)
    file_replaces_file_id = Column(UNIQUEIDENTIFIER)
    is_soft_deleted = Column(Boolean, default=False)
    is_hard_deleted = Column(Boolean, default=False)
    file_extension = Column(String(4), nullable=False)
    last_access_date = Column(DateTime)
    last_checked_for_malware = Column(DateTime)
    file_accessed_times = Column(Integer)
    SHA_256_hash = Column(String(64))
    public_access_token_url_suffix = Column(String(255))
    viewable_by_anyone_with_public_access_token = Column(Boolean, default=False)
    is_data_pull_needed = Column(Boolean, default=False)
    deleted_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"<File(id={self.file_id}, name={self.file_name})>"

# Pydantic models
class FileBase(BaseModel):
    file_id: UUID4
    file_upload_pending: bool
    file_privacy_type_choice: UUID4
    file_is_linked_to_table: str
    file_is_linked_to_id: UUID4
    file_type_choice: UUID4
    file_sub_type_choice: UUID4
    file_size_kb: PositiveInt
    file_name: str
    file_owner_entity_id: UUID4
    file_uploaded_by_id: UUID4
    file_uploaded_on: datetime
    file_replaces_file_id: UUID4
    is_soft_deleted: bool
    is_hard_deleted: bool
    file_extension: constr(max_length=4)
    last_access_date: datetime
    last_checked_for_malware: datetime
    file_accessed_times: int
    SHA_256_hash: constr(max_length=64)
    public_access_token_url_suffix: str
    viewable_by_anyone_with_public_access_token: bool
    is_data_pull_needed: bool
    deleted_at: datetime = None
    created_at: datetime
    updated_at: datetime

    @validator("file_uploaded_on", "last_access_date", "last_checked_for_malware", pre=True, always=True)
    def parse_uploaded_on(cls, v):
        return datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f")

    class Config:
        orm_mode = True

class FileCreate(FileBase):
    pass

class FileUpdate(BaseModel):
    file_upload_pending: Optional[bool]
    file_privacy_type_choice: Optional[UUID4]
    file_is_linked_to_table: Optional[str]
    file_is_linked_to_id: Optional[UUID4]
    file_type_choice: Optional[UUID4]
    file_sub_type_choice: Optional[UUID4]
    file_size_kb: Optional[PositiveInt]
    file_name: Optional[str]
    file_owner_entity_id: Optional[UUID4]
    file_uploaded_by_id: Optional[UUID4]
    file_uploaded_on: Optional[datetime]
    file_replaces_file_id: Optional[UUID4]
    is_soft_deleted: Optional[bool]
    is_hard_deleted: Optional[bool]
    file_extension: Optional[str]
    last_access_date: Optional[datetime]
    last_checked_for_malware: Optional[datetime]
    file_accessed_times: Optional[int]
    SHA_256_hash: Optional[str]
    public_access_token_url_suffix: Optional[str]
    viewable_by_anyone_with_public_access_token: Optional[bool]
    is_data_pull_needed: Optional[bool]
    deleted_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


