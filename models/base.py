from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import as_declarative

meta = sa.MetaData()


@as_declarative(metadata=meta)
class BaseModelORM:
    __abstract__ = True
    created_at = sa.Column(
        sa.DateTime, default=datetime.utcnow, server_default=sa.func.now()
    )
    updated_at = sa.Column(
        sa.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=sa.func.now(),
    )
    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
