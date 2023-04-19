import asyncio

from betexplorerparser.utils.league_list_keeper import LeagueListKeeper
from betexplorerparser.utils.url_maker import UrlMaker


class BetExplorerParser:
    def __init__(self, max_workers: int = None):
        self._max_workers = max_workers
        self._league_list_keeper = LeagueListKeeper()
        self._url_maker = UrlMaker()
        self._request = Request()

    def parse_all(self) -> None:
        leagues = self._league_list_keeper.get_leagues()
        urls = self._url_maker.get_result_urls(leagues)
        pages = self._request.get(urls)
        pages = asyncio.run(self._parse_async)



