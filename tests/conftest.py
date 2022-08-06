import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import create_database, drop_database
from starlette.testclient import TestClient

from database import SQLALCHEMY_DATABASE_URL
from database import get_db
from models.base import meta
from run import create_app


@pytest.fixture()
def test_session_maker() -> sessionmaker:
    testing_database_url = SQLALCHEMY_DATABASE_URL + '_testing_' + str(uuid.uuid4())
    create_database(testing_database_url)
    try:
        engine = create_engine(testing_database_url)
        testing_session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        meta.create_all(bind=engine)
        yield testing_session_maker
    finally:
        drop_database(testing_database_url)


@pytest.fixture()
def db(test_session_maker) -> Session:
    session = test_session_maker()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def test_client(db: Session) -> TestClient:
    fastapi_app = create_app()
    fastapi_app.dependency_overrides[get_db] = lambda: db
    with TestClient(fastapi_app) as client:
        yield client
