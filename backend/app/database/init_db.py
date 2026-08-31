from app.database.database import Base, engine
from app.models.user import User
from app.models.attack_log import AttackLog

print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")