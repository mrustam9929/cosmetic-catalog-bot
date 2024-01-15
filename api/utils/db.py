from typing import Generator
from core.database import Session


def get_db() -> Generator:
    db = Session()
    try:
        yield db
    finally:
        db.close()

