from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db():
    # Import models to ensure they are registered with SQLAlchemy's metadata
    import database.models  # noqa: F401
    Base.metadata.create_all(bind=engine)


# Create tables at import time
init_db()
