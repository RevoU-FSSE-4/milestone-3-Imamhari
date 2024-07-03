from models.base import Base

from sqlalchemy import Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

class Transaction(Base):
    __tablename__ = "transactions"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    from_account_id = mapped_column(Integer, ForeignKey("accounts.id"), nullable=False)
    to_account_id = mapped_column(Integer, ForeignKey("accounts.id"), nullable=False)
    amount = mapped_column(Integer, nullable=False)
    type = mapped_column(String(255), nullable=False)
    description = mapped_column(Text)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    