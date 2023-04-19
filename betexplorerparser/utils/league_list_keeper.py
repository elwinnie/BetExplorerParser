import json
import os
from pathlib import Path


class LeagueListKeeper:
    _LEAGUE_FILE = Path("betexplorerparser/leagues.json")

    def __init__(self):
        self._default_leagues = [{"country": "russia", "league": "premier-league", "start": 2013},
                                 {"country": "england", "league": "premier-league", "start": 2011},
                                 {"country": "germany", "league": "bundesliga", "start": 2011},
                                 {"country": "france", "league": "ligue-1", "start": 2011},
                                 {"country": "spain", "league": "laliga", "start": 2011},
                                 {"country": "italy", "league": "serie-a", "start": 2011},
                                 {"country": "belgium", "league": "jupiler-pro-league", "start": 2021},
                                 {"country": "portugal", "league": "liga-portugal", "start": 2014},
                                 {"country": "netherlands", "league": "eredivisie", "start": 2014},
                                 {"country": "turkey", "league": "super-lig", "start": 2011},
                                 {"country": "austria", "league": "bundesliga", "start": 2011},
                                 {"country": "greece", "league": "super-league", "start": 2017}]

    def get_leagues(self):
        """
        The get_leagues function returns a list of leagues that are currently being tracked.
        The function first checks to see if the league file exists, and if it does not, creates one with default values.
        If the file does exist, then it reads in the contents of the file and returns them as a list.

        :param self: Refer to the object itself
        :return: A list of dictionaries, where each dictionary is a league
        """
        if not os.path.exists(self._LEAGUE_FILE):
            self._make_league_file()
            return self._default_leagues
        with open(self._LEAGUE_FILE, 'r', encoding='utf-8') as inf:
            leagues = json.loads(inf.read())
        return leagues

    def _make_league_file(self, leagues: dict = None) -> bool:
        try:
            with open(self._LEAGUE_FILE, 'w', encoding='utf-8') as ouf:
                if leagues:
                    js = json.dumps(leagues, indent=4, ensure_ascii=False)
                else:
                    js = json.dumps(self._default_leagues, indent=4, ensure_ascii=False)
                ouf.write(js)
        except Exception as e:
            print(e)
            return False
        return True

    def add_league(self, country: str, league: str) -> bool:
        """
        The add_league function adds a new league to the leagues.json file.

        :param self: Refer to the object itself
        :param country: str: Specify the country of the league
        :param league: str: Add the league name to the list of leagues
        :return: True if the league is added to the file and false if it already exists
        """
        leagues = self.get_leagues()
        new_league = {"country": country, "league": league}
        for league_in_list in leagues:
            if league_in_list["country"] == country and league_in_list["league"] == league:
                return False
        leagues.append(new_league)
        return self._make_league_file(leagues)

    def remove_league(self, country: str, league: str) -> bool:
        """
        The remove_league function removes a league from the leagues.json file.

        :param self: Refer to the object itself
        :param country: str: Specify the country of the league to be removed
        :param league: str: Specify which league to remove from the list
        :return: True if the league is successfully removed,
        """
        leagues = self.get_leagues()
        for league_in_list in leagues:
            if league_in_list["country"].lower() == country.lower() and \
                    league_in_list["league"].lower() == league.lower():
                leagues.remove(league_in_list)
                break
        else:
            return False
        return self._make_league_file(leagues)
