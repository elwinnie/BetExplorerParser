from bs4 import BeautifulSoup


class ResultParser:
    def parse(self, result_page: str, fixtures_page: str = None) -> dict:
        """
        The parse function takes the result page and fixtures page as input,
            parses them and returns a dictionary with three keys:
                - is_all_ids_parsed (boolean)
                - results (dict)
                - fixtures (dict)

        :param self: Represent the instance of the class
        :param result_page: str: Pass the page of results to be parsed
        :param fixtures_page: str: Pass the page of fixtures to be parsed
        :return: A dict with three keys:
        """

        results = self._parse_results(result_page)
        fixtures = self._parse_results(fixtures_page)
        if fixtures:
            is_all_ids_parsed = True if fixtures["total_tours"] == fixtures["games"][-1]["tour"] else False
        else:
            is_all_ids_parsed = True if results["total_tours"] == results["games"][-1]["tour"] else False

        return {"is_all_ids_parsed": is_all_ids_parsed, "results": results, "fixtures": fixtures}

    @staticmethod
    def _parse_results(result_page: str) -> dict:
        soup = BeautifulSoup(result_page, "lxml")
        league = soup.find("h1").span.text.strip()[:-9].strip()
        season = int(soup.find("h1").span.text.strip()[-9:-5])
        try:
            tour = None
            total_tours = None
            games = []
            match_count = 0

            for row in soup("div", class_="box-overflow")[1].find_all("tr", class_="")[:-1]:
                if tour_block := row.find("th"):
                    tour = int(tour_block.text.split(".")[0])
                    if match_count and not total_tours:
                        total_tours = (match_count * 2 - 1) * 2
                    continue
                match_count += 1
                home_team, away_team = [team.text for team in row.find("td", class_="h-text-left").find_all("span")]
                match_id = row.find("td", class_="h-text-left").a["href"].split("/")[-2].strip()
                games.append({
                    "id": match_id, "tour": tour, "home_team": home_team, "away_team": away_team
                })
            games = sorted(games, key=lambda x: x["tour"])
        except AttributeError as e:
            total_tours = None
            games = None
            print(e)

        return {"league": league, "season": season, "total_tours": total_tours, "games": games}
