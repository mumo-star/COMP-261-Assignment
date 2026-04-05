from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Database configuration
DATABASE_URL = "sqlite:///./student_management.db"

#Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

#Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

#Base class for models
Base = declarative_base()

def get_db():
    """
    Dependency function to get database session.
    
    Yields:
        Session: Database session for the request lifecycle
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
