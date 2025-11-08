from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import config

engine = create_engine(config.DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()