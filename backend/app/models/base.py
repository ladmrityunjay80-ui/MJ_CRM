"""
Base model with common fields
"""

from datetime import datetime
from sqlalchemy import Column, DateTime, func
from app.core.database import Base


class TimestampMixin:
    """Mixin for adding timestamp fields to models"""
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
