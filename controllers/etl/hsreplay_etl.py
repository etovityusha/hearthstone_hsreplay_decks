import datetime
from typing import List, TypedDict

import requests
import sqlalchemy.orm
from bs4 import BeautifulSoup
from pydantic import BaseModel

from controllers.chrome_wrapper import ChromeWrapper
from controllers.etl.etl_abc import ETLBase
from models.deck import ETLDeck
from models.etl_run import ETLRun


class HSReplayArchetype(BaseModel):
    id: int
    name: str
    url: str


class HsReplayDeck(BaseModel):
    archetype: HSReplayArchetype
    cards: List[int]


class DeckURL(BaseModel):
    url: str


class ArchetypeDeckURLs(BaseModel):
    archetype: HSReplayArchetype
    urls: List[DeckURL]


class ETLResult(TypedDict):
    etl_run: ETLRun
    etl_decks: List[ETLDeck]


class HSReplayETL(ETLBase):
    def __init__(
            self,
            session: sqlalchemy.orm.Session,
            heroes: tuple = ('demonhunter', 'druid', 'hunter', 'mage', 'paladin', 'priest', 'rogue', 'shaman',
                             'warlock', 'warrior'),
            proxy: str = None,
    ):
        self.heroes = heroes
        self.session = session
        self.requests_session = requests.Session()
        self.proxy = proxy
        if self.proxy:
            self.requests_session.proxies.update(self.proxy)

    def _extract(self) -> List[HsReplayDeck]:
        decks = []
        with ChromeWrapper(proxy=self.proxy) as self.driver:
            archetypes = self.__get_archetypes_list()
            archetypes_with_deck_urls = [self.__get_decks_urls(archetype) for archetype in archetypes]
            for archetype_with_deck_urls in archetypes_with_deck_urls:
                decks.extend([self.__get_deck_info_from_url(
                    deck_url=deck_url,
                    archetype=archetype_with_deck_urls.archetype
                ) for deck_url in archetype_with_deck_urls.urls])
        return decks

    def _load(self, transformed: List[HsReplayDeck]) -> ETLResult:
        decks = []
        etl_run = ETLRun(date=datetime.datetime.utcnow().date(), is_completed=False)
        self.session.add(etl_run)
        for deck in transformed:
            etl_deck = ETLDeck(etl_run=etl_run, archetype_name=deck.archetype.name, cards=deck.cards)
            self.session.add(etl_deck)
            decks.append(etl_deck)
        etl_run.is_completed = True
        self.session.commit()
        return ETLResult(etl_run=etl_run, etl_decks=decks)

    def __get_archetypes_list(self) -> List[HSReplayArchetype]:
        self.driver.get('https://hsreplay.net/meta/#tab=archetypes')
        soup = BeautifulSoup(self.driver.page_source, features="html.parser")
        result = []
        for class_name in self.heroes:
            elements = soup.find_all('a', f'player-class {class_name}')
            result.extend([HSReplayArchetype(
                id=int(''.join(i for i in el['href'] if i.isdigit())),
                name=el.text,
                url=el['href'],
            ) for el in elements])
        return result

    def __get_decks_urls(self, archetype: HSReplayArchetype) -> ArchetypeDeckURLs:
        self.driver.get(f'https://hsreplay.net{archetype.url}#tab=similar')
        soup = BeautifulSoup(self.driver.page_source, features="html.parser")
        decks = soup.find_all('a', {'class': 'deck-tile'})
        urls = [DeckURL(url=x['href']) for x in decks]
        return ArchetypeDeckURLs(archetype=archetype, urls=urls)

    def __get_deck_info_from_url(self, deck_url: DeckURL, archetype: HSReplayArchetype) -> HsReplayDeck:
        req = self.requests_session.get(f'https://hsreplay.net{deck_url.url}')
        soup = BeautifulSoup(req.text)
        deck_info = soup.find('div', {'id': 'deck-info'})
        return HsReplayDeck(archetype=archetype, cards=list(map(int, deck_info.attrs['data-deck-cards'].split(','))))
