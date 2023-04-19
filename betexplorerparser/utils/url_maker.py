from datetime import datetime


class UrlMaker:
    _RESULTS_PAGE_URL = "https://www.betexplorer.com/soccer/{country}/{league}/results/"
    _FIXTURES_PAGE_URL = "https://www.betexplorer.com/soccer/{country}/{league}/fixtures/"

    def __init__(self):
        current_date = datetime.now().date()
        target_month = 6
        self._last_season_year = current_date.year if current_date.month > target_month else current_date.year - 1

    def get_result_urls(self, leagues: list[dict]) -> list[tuple[str, str]]:
        """
        The function takes a list of leagues and returns a list of tuples containing
        the results and fixtures urls for each league.

        :param self: Refer to the current instance of a class
        :param leagues: list[dict]: Pass in a list of dictionaries that contain the country,
            league and start year for each league
        :return: A list of tuples, where each tuple contains the url for results and fixtures
        """

        urls = []
        for league in leagues:
            for year in range(league["start"], self._last_season_year):
                results_url = self._RESULTS_PAGE_URL.format(country=league["country"],
                                                            league=f"{league['league']}-{year}-{year + 1}")
                fixtures_url = self._FIXTURES_PAGE_URL.format(country=league["country"],
                                                              league=f"{league['league']}-{year}-{year + 1}")
                urls.append((results_url, fixtures_url))
            else:
                results_url = self._RESULTS_PAGE_URL.format(country=league["country"], league=league["league"])
                fixtures_url = self._FIXTURES_PAGE_URL.format(country=league["country"],
                                                              league=league["league"])
                urls.append((results_url, fixtures_url))
        return urls
