from models.base import Base

from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column



class Account(Base):
    __tablename__ = "accounts"
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), ondelete="CASCADE")
    account_type = mapped_column(String(255), nullable=False)
    account_number = mapped_column(String(255), nullable=False)
    balance = mapped_column(Integer, nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=False)
    