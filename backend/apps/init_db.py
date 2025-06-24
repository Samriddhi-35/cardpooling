from models import Base
from db import engine

# Create tables in the DB
Base.metadata.create_all(bind=engine)

print(" All tables created successfully.")
