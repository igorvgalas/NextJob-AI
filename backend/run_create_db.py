# run_create_db.py
from app.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)
