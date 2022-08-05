from collections import defaultdict

import sqlalchemy as sa
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.decks.schemas import ETLResult, ArchetypeDecks
from database import get_db
from models.etl_run import ETLRun
from models.deck import ETLDeck

router = APIRouter(
    prefix="/decks",
    dependencies=[],
    tags=["decks"]
)


@router.get("", response_model=ETLResult)
async def etl_run_info(_id: int = None, db: Session = Depends(get_db)):
    if not _id:
        etl = db.query(ETLRun).filter_by(is_completed=True).order_by(sa.desc(ETLRun.id)).first()
    else:
        etl = db.query(ETLRun).filter_by(id=_id, is_completed=True).first()
    if not etl:
        raise HTTPException(status_code=404, detail="ETL run not found or not completed")
    decks = db.query(ETLDeck).filter_by(etl_run=etl).all()
    dfltdct = defaultdict(list)
    for deck in decks:
        dfltdct[deck.archetype_name].append(deck.cards)
    return ETLResult(etl_id=etl.id, etl_date=etl.date,
                     archetypes=[ArchetypeDecks(archetype_title=k, decks=v) for k, v in dfltdct.items()])
