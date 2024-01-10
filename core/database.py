from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker

from core.config import settings

engine = create_engine(settings.db_url, max_overflow=50, pool_pre_ping=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:
    __name__: str

