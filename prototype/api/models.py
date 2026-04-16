from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, Enum
from sqlalchemy.sql import func
from database import Base
import enum

class AgentStatus(str, enum.Enum):
    pending_review = "pending_review"
    active = "active"
    suspended = "suspended"
    retired = "retired"

class RiskLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"
    
class Agent(Base):
    __tablename__ = "agents"

    agent_id       = Column(String, primary_key=True, index=True)
    agent_name     = Column(String, nullable=False)
    agent_type     = Column(String, nullable=False)
    owner_id       = Column(String, nullable=False)
    owner_email    = Column(String, nullable=False)
    business_unit  = Column(String, nullable=False)
    use_case       = Column(Text, nullable=False)
    data_classification = Column(String, nullable=False)
    autonomy_level = Column(Integer, nullable=False)
    external_exposure = Column(Boolean, default=False)
    framework      = Column(String, nullable=False)
    deployment_env = Column(String, nullable=False)
    eol_date       = Column(DateTime, nullable=False)
    risk_score     = Column(Integer, default=0)
    risk_level     = Column(Enum(RiskLevel), default=RiskLevel.low)
    status         = Column(Enum(AgentStatus), default=AgentStatus.pending_review)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())
    last_reviewed  = Column(DateTime(timezone=True), nullable=True)
    
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    agent_id     = Column(String, nullable=False)
    action       = Column(String, nullable=False)
    performed_by = Column(String, nullable=False)
    detail       = Column(Text, nullable=True)
    timestamp    = Column(DateTime(timezone=True), server_default=func.now())