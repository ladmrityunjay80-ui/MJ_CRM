"""
Comment Model
Represents comments and mentions for team collaboration
"""

from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class Comment(Base, TimestampMixin):
    """Comment model for team collaboration"""
    
    __tablename__ = "comments"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    
    # Entity reference
    entity_type = Column(String, nullable=False, index=True)  # lead, contact, deal, etc.
    entity_id = Column(String, nullable=False, index=True)
    
    # Parent comment for threading
    parent_id = Column(String, ForeignKey("comments.id"), nullable=True)
    
    # Organization and user
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Mentions (JSON array of user IDs)
    mentions = Column(Text, nullable=True)
    
    # Relationships
    organization = relationship("Organization")
    user = relationship("User")
    parent = relationship("Comment", remote_side=[id])
    replies = relationship("Comment", back_populates="parent")
    
    def __repr__(self):
        return f"<Comment(id={self.id}, entity_type={self.entity_type}, entity_id={self.entity_id})>"
