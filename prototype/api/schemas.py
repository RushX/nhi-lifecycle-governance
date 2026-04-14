from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from models import AgentStatus, RiskLevel

class AgentCreate(BaseModel):
    agent_name: str
    agent_type: str
    owner_id: str
    owner_email: str
    business_unit: str
    use_case: str
    data_classification: str
    autonomy_level: int
    external_exposure: bool
    framework: str
    deployment_env: str
    eol_date: datetime

class AgentResponse(BaseModel):
    agent_id: str
    agent_name: str
    agent_type: str
    owner_id: str
    owner_email: str
    business_unit: str
    use_case: str
    data_classification: str
    autonomy_level: int
    external_exposure: bool
    framework: str
    deployment_env: str
    eol_date: datetime
    risk_score: int
    risk_level: RiskLevel
    status: AgentStatus
    created_at: datetime
    last_reviewed: Optional[datetime]

    class Config:
        from_attributes = True
        

class StatusUpdate(BaseModel):
    status: AgentStatus
    performed_by: str
    reason: Optional[str] = None

class AuditLogResponse(BaseModel):
    id: int
    agent_id: str
    action: str
    performed_by: str
    detail: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True