from unittest.mock import patch

from controllers.etl.hsreplay_etl import HSReplayETL, HsReplayDeck, HSReplayArchetype
from models.deck import ETLDeck
from models.etl_run import ETLRun


@patch('controllers.etl.hsreplay_etl.HSReplayETL._extract')
def test_transform_and_load(extract_mock, db):
    extract_mock.return_value = [HsReplayDeck(
        archetype=HSReplayArchetype(id=idx, name=f'druid_{idx}', url=f'druid_{idx}'),
        cards=list(range(1, 31)),
    ) for idx in range(1, 6)]
    result = HSReplayETL(session=db, heroes=('druid',), proxy=None).execute()
    assert len(result['etl_decks']) == 5

    assert db.query(ETLRun).count() == 1
    assert result['etl_run'] == db.query(ETLRun).first()
    assert db.query(ETLDeck).count() == 5
