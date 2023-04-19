import aiohttp

from betexplorerparser.bet_explorer_parser import BetExplorerParser

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
    # 'x-requested-with': 'XMLHttpRequest',
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
    bexp = BetExplorerParser()
    bexp.parse_all(None)
