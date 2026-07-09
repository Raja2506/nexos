from app.database import SessionLocal
from app.models.db_models import User

def test_insert_and_query_user():
    db = SessionLocal()
    user = User(email="test@nexos.com", name="Test User", auth_provider="local")
    db.add(user)
    db.commit()

    fetched = db.query(User).filter_by(email="test@nexos.com").first()
    assert fetched is not None
    assert fetched.name == "Test User"

    db.delete(fetched)
    db.commit()
    db.close()