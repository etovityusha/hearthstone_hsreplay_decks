import datetime
from typing import List

from pydantic import BaseModel, Field


class ArchetypeDecks(BaseModel):
    archetype_title: str = Field(None, example='Control Warrior')
    decks: List[List[int]] = Field(None, example=[list(range(1, 31)), list(range(31, 61))])


class ETLResult(BaseModel):
    etl_id: int
    etl_date: datetime.date
    archetypes: List[ArchetypeDecks]
