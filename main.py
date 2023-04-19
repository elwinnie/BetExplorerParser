from unittest import result

import aiohttp
import asyncio
from bs4 import BeautifulSoup
from betexplorerparser.parsers.odds_parser import OddsParser
from betexplorerparser.parsers.result_parser import ResultParser
from betexplorerparser.utils.league_list_keeper import LeagueListKeeper
from betexplorerparser.utils.url_maker import UrlMaker

x12_url = 'https://www.betexplorer.com/match-odds/IPjYcWzM/1/1x2/'
dnb_url = 'https://www.betexplorer.com/match-odds/lEUGk8r2/1/ha/'
dc_url = 'https://www.betexplorer.com/match-odds/IPjYcWzM/1/dc/'
bts_url = 'https://www.betexplorer.com/match-odds/IPjYcWzM/1/bts/'
ou_url = 'https://www.betexplorer.com/match-odds/IPjYcWzM/1/ou/'
ah_url = 'https://www.betexplorer.com/match-odds/lEUGk8r2/1/ah/'
page_url = 'https://www.betexplorer.com/soccer/russia/premier-league/lokomotiv-moscow-zenit-st-petersburg/IPjYcWzM/'

result_url = 'https://www.betexplorer.com/soccer/russia/premier-league/results/'
fixtures_url = 'https://www.betexplorer.com/soccer/russia/premier-league/fixtures/'

headers = {
    'referer': 'https://www.betexplorer.com/soccer/russia/premier-league/lokomotiv-moscow-zenit-st-petersburg/IPjYcWzM/',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}


async def main(url: str):
    async with aiohttp.ClientSession(trust_env=False) as session:
        async with session.get(url, headers=headers) as resp:
            page = await resp.text()
    return page


def clear_page(page: str) -> str:
    page = page[page.find("<"):page.rfind(">") + 1]
    page = page.replace(r'\"', '"')
    page = page.replace(r'\/', '/')
    page = page.replace(r'\n', '')

    return page


if __name__ == '__main__':
    league_keeper = LeagueListKeeper()
    url_maker = UrlMaker()
    print(url_maker.get_result_urls(league_keeper.get_leagues()))

    # bexp = ResultParser()
    # result_page = asyncio.run(main(result_url))
    # fixtures_page = asyncio.run(main(fixtures_url))
    # print(bexp.parse(result_page, fixtures_page))

    # page = asyncio.run(main(page_url))
    # x12 = asyncio.run(main(x12_url))
    # dnb = asyncio.run(main(dnb_url))
    # dc = asyncio.run(main(dc_url))
    # bts = asyncio.run(main(bts_url))
    # ou = asyncio.run(main(ou_url))
    # ah = asyncio.run(main(ah_url))
    #
    # page = clear_page(page)
    # x12 = clear_page(x12)
    # dnb = clear_page(dnb)
    # dc = clear_page(dc)
    # bts = clear_page(bts)
    # ou = clear_page(ou)
    # ah = clear_page(ah)
    # bexp = OddsParser()
    # print(bexp.parse(page, x12, ou, ah, dnb, dc, bts))
