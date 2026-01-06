from app.db.database import engine
from app.db.models import base

base.metadata.create_all(bind=engine)
print("tables created")
