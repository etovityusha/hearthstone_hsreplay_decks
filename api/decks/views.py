import sqlalchemy as sa
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from controllers.etl.dto import ETLResult
from controllers.etl.generate_result import ETLResultGenerator
from database import get_db
from models.etl_run import ETLRun

router = APIRouter(
    prefix="/decks",
    dependencies=[],
    tags=["decks"]
)


@router.get("", response_model=ETLResult)
async def last_completed_etl_result(_id: int = None, db: Session = Depends(get_db)):
    etl = db.query(ETLRun).filter_by(is_completed=True).order_by(sa.desc(ETLRun.id)).first()
    if not etl:
        raise HTTPException(status_code=404, detail="ETL run not found or not completed")
    return ETLResultGenerator(db, etl).generate()
