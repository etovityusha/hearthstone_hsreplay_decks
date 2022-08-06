from collections import defaultdict

from sqlalchemy.orm import Session

from controllers import etl
from controllers.etl.dto import ArchetypeDecks, ETLResult
from models.deck import ETLDeck
from models.etl_run import ETLRun


class ETLResultGenerator:
    def __init__(self, session: Session, etl_run: ETLRun):
        self.session = session
        self.etl_run = etl_run

    def generate(self) -> ETLResult:
        decks = self.session.query(ETLDeck).filter_by(etl_run=etl).all()
        result = defaultdict(list)
        for deck in decks:
            result[deck.archetype_name].append(deck.cards)
        return ETLResult(
            etl_id=self.etl_run.id,
            etl_date=self.etl_run.date,
            archetypes=[ArchetypeDecks(archetype_title=k, decks=v) for k, v in result.items()]
        )
