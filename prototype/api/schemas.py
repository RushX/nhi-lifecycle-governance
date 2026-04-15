from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional,Literal
from models import AgentStatus, RiskLevel

class AgentCreate(BaseModel):
    agent_name: str
    registered_by: str
    # Agent type is captured as metadata for filtering and audit purposes. I deliberately excluded it from scoring because it overlaps with autonomy level — both measure behavioral risk. Adding it would double-count that dimension and inflate scores for autonomous agents. I noted it as a v2.0 consideration pending empirical validation.
    agent_type: Literal["copilot", "autonomous", "api-connected", "workflow"]
    owner_id: str
    owner_email: str
    business_unit: str
    use_case: str
    data_classification: Literal["public", "internal", "confidential", "restricted"]
    autonomy_level: int = Field(..., ge=1, le=5)
    external_exposure: bool
    framework: str
    deployment_env: Literal["development", "staging", "production"]
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
        
class CertifyRequest(BaseModel):
    performed_by: str
    notes: Optional[str] = None