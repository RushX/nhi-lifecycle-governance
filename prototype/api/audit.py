from models import AuditLog
from sqlalchemy.orm import Session

def log_event(db: Session, agent_id: str, action: str,
              performed_by: str, detail: str = None):
    entry = AuditLog(
        agent_id=agent_id,
        action=action,
        performed_by=performed_by,
        detail=detail
    )
    db.add(entry)
    db.commit()