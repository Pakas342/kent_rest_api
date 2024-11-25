from typing import Annotated

from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session


DATABASE_URL = "postgresql+psycopg://postgres:305042@localhost:5432/kent_institute_crud"

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True, pool_size=5, max_overflow=10)


def create_db_structure():
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            raise e
        finally:
            session.close()


SessionDep = Annotated[Session, Depends(get_session)]
