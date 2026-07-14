from app.db.database import engine
from app.db.database import Base

from app.models.user import User
from app.models.agent import Agent

Base.metadata.create_all(bind=engine)

print("Tables created.")