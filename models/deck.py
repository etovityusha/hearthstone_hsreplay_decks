import sqlalchemy as sa
from sqlalchemy.orm import relationship, validates

from models.base import BaseModelORM
from models.etl_run import ETLRun


class ETLDeck(BaseModelORM):
    __tablename__ = 'etl_decks'

    etl_run = relationship(ETLRun)
    etl_run_id = sa.Column(sa.ForeignKey(ETLRun.id), nullable=False)
    archetype_name = sa.Column(sa.String, nullable=False)
    cards = sa.Column(sa.ARRAY(sa.Integer), nullable=False, default=[])

    @validates('cards')
    def validate_name(self, key, value):
        assert len(value) == 30
        return value
