import asyncio

from betexplorerparser.parsers.result_parser import ResultParser
from betexplorerparser.utils.league_list_keeper import LeagueListKeeper
from betexplorerparser.utils.request import Request
from betexplorerparser.utils.url_maker import UrlMaker


class BetExplorerParser:
    def __init__(self, max_workers: int = None):
        self._max_workers = max_workers
        self._league_list_keeper = LeagueListKeeper()
        self._url_maker = UrlMaker()
        self._request = Request()

        self._result_parser = ResultParser()

    def parse_all(self, output_dir: str) -> None:
        leagues = self._league_list_keeper.get_leagues()
        urls = self._url_maker.get_result_urls(leagues)
        pages = self._request.get(urls, desc="Result requests")
        parsed_pages = []
        for page_set in pages:
            if page_set:
                parsed_pages.append(self._result_parser.parse(*page_set))





