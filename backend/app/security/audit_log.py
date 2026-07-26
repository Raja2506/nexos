from sqlalchemy.orm import Session
from app.models.db_models import AuditLog

def log_action(db: Session, action: str, resource: str = None, user_id: str = None, ip_address: str = None):
    entry = AuditLog(
        user_id=user_id,
        action=action,
        resource=resource,
        ip_address=ip_address,
    )
    db.add(entry)
    db.commit()