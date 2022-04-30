import sqlalchemy as sa

from core.models.base import BaseModelORM


class ETLRun(BaseModelORM):
    __tablename__ = 'etl_runs'

    date = sa.Column(sa.Date)
    is_completed = sa.Column(sa.Boolean, default=False)
