from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Base de données SQLite
DATABASE_URL = "sqlite:///./action_verite.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()