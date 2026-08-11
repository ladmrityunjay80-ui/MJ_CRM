"""
Workflow Model
Represents automated workflows for CRM operations
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin
import enum


class TriggerType(str, enum.Enum):
    """Types of workflow triggers"""
    LEAD_CREATED = "lead_created"
    LEAD_UPDATED = "lead_updated"
    LEAD_STATUS_CHANGED = "lead_status_changed"
    DEAL_CREATED = "deal_created"
    DEAL_UPDATED = "deal_updated"
    DEAL_STAGE_CHANGED = "deal_stage_changed"
    CONTACT_CREATED = "contact_created"
    ACTIVITY_CREATED = "activity_created"
    ACTIVITY_COMPLETED = "activity_completed"
    SCHEDULED = "scheduled"


class ActionType(str, enum.Enum):
    """Types of workflow actions"""
    SEND_EMAIL = "send_email"
    CREATE_TASK = "create_task"
    UPDATE_FIELD = "update_field"
    ASSIGN_USER = "assign_user"
    ADD_TAG = "add_tag"
    REMOVE_TAG = "remove_tag"
    CREATE_NOTE = "create_note"
    WEBHOOK = "webhook"
    CUSTOM = "custom"


class WorkflowStatus(str, enum.Enum):
    """Workflow execution status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DRAFT = "draft"


class Workflow(Base, TimestampMixin):
    """Workflow model for automation"""
    
    __tablename__ = "workflows"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Trigger configuration
    trigger_type = Column(SQLEnum(TriggerType), nullable=False)
    trigger_config = Column(Text, nullable=True)  # JSON string for trigger conditions
    
    # Workflow status
    status = Column(SQLEnum(WorkflowStatus), default=WorkflowStatus.DRAFT)
    
    # Organization
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False, index=True)
    
    # Relationships
    organization = relationship("Organization", back_populates="workflows")
    actions = relationship("WorkflowAction", back_populates="workflow", cascade="all, delete-orphan")
    executions = relationship("WorkflowExecution", back_populates="workflow", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Workflow(id={self.id}, name={self.name}, trigger_type={self.trigger_type})>"


class WorkflowAction(Base, TimestampMixin):
    """Individual action within a workflow"""
    
    __tablename__ = "workflow_actions"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    workflow_id = Column(String, ForeignKey("workflows.id"), nullable=False, index=True)
    
    # Action configuration
    action_type = Column(SQLEnum(ActionType), nullable=False)
    action_config = Column(Text, nullable=False)  # JSON string for action parameters
    order = Column(String, nullable=False)  # Execution order
    
    # Relationships
    workflow = relationship("Workflow", back_populates="actions")
    
    @property
    def action_config_dict(self):
        """Parse action_config JSON string to dictionary"""
        import json
        if self.action_config:
            return json.loads(self.action_config)
        return {}
    
    def __repr__(self):
        return f"<WorkflowAction(id={self.id}, action_type={self.action_type}, order={self.order})>"


class WorkflowExecution(Base, TimestampMixin):
    """Record of workflow execution"""
    
    __tablename__ = "workflow_executions"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    workflow_id = Column(String, ForeignKey("workflows.id"), nullable=False, index=True)
    
    # Execution details
    trigger_entity_id = Column(String, nullable=True)  # ID of entity that triggered workflow
    trigger_entity_type = Column(String, nullable=True)  # Type of entity (lead, deal, etc.)
    
    # Execution status
    status = Column(String, nullable=False)  # running, completed, failed
    result = Column(Text, nullable=True)  # JSON string with execution results
    error_message = Column(Text, nullable=True)
    
    # Timing
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    workflow = relationship("Workflow", back_populates="executions")
    
    def __repr__(self):
        return f"<WorkflowExecution(id={self.id}, workflow_id={self.workflow_id}, status={self.status})>"
