import os
from typing import TYPE_CHECKING

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

if TYPE_CHECKING:
    from sqlalchemy import Engine

load_dotenv()

SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL")

engine: Engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
