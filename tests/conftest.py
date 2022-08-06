import uuid

import alembic
import pytest
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, drop_database
from starlette.testclient import TestClient

from database import get_db
from models.base import meta
from run import create_app


@pytest.fixture()
def test_client():
    fastapi_app = create_app()
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/test-fastapi-test"
    # if not database_exists(SQLALCHEMY_DATABASE_URL):
    create_database(SQLALCHEMY_DATABASE_URL)
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    meta.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    fastapi_app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(fastapi_app)
    finally:
        drop_database(SQLALCHEMY_DATABASE_URL)


def create_test_database(base_sqlalchemy_url: str) -> None:
    database_id = str(uuid.uuid4())
    dsn = f"{base_sqlalchemy_url}_testing_{database_id}"
    try:
        create_database(dsn)
        alembic_cfg = Config(file_='migrations/alembic.ini')
        alembic_cfg.set_main_option("script_location", "migrations")
        alembic_cfg.set_main_option("sqlalchemy.url", dsn)
        alembic.command.upgrade(config=alembic_cfg, revision="head")
        yield dsn
    finally:
        drop_database(dsn)
