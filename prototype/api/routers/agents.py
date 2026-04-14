import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Agent, AuditLog
from schemas import AgentCreate, AgentResponse, StatusUpdate, AuditLogResponse

router = APIRouter(prefix="/agents", tags=["agents"])
@router.post("/", response_model=AgentResponse, status_code=201)

def register_agent(payload: AgentCreate, db: Session = Depends(get_db)):
    agent_id = str(uuid.uuid4())
    agent = Agent(
        agent_id=agent_id,
        **payload.model_dump()
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent
