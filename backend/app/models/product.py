"""
Product Model
Represents products and services that can be sold
"""

from sqlalchemy import Column, String, Float, Text, ForeignKey, Enum as SQLEnum, Integer, Boolean
from sqlalchemy.orm import relationship
from enum import Enum
from app.core.database import Base
from app.models.base import TimestampMixin


class ProductType(str, Enum):
    """Product type options"""
    PRODUCT = "product"
    SERVICE = "service"
    SUBSCRIPTION = "subscription"
    MAINTENANCE = "maintenance"
    OTHER = "other"


class Product(Base, TimestampMixin):
    """Product model"""
    
    __tablename__ = "products"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    sku = Column(String, unique=True, index=True, nullable=True)
    
    # Type and pricing
    type = Column(SQLEnum(ProductType), default=ProductType.PRODUCT, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, default="USD", nullable=False)
    
    # Inventory (for products)
    quantity_in_stock = Column(Integer, nullable=True)
    low_stock_threshold = Column(Integer, nullable=True)
    
    # Additional info
    notes = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)  # JSON array of tags
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Foreign Keys
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False)
    
    # Relationships
    organization = relationship("Organization", back_populates="products")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, type={self.type}, price={self.price})>"
