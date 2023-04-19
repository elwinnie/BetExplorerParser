from datetime import datetime

from bs4 import BeautifulSoup


class OddsParser:
    def parse(self, page: str, x12: str, ou: str, ah: str, dnb: str, dc: str, bts: str) -> dict:
        """
        The parse function takes the page and odds tables and returns dictionary with data

        :param self: Represent the instance of the class
        :param page: str: Parse the match info, such as date and time
        :param x12: str: Parse the 1x2 odds
        :param ou: str: Parse over under odds
        :param ah: str: Parse the asian handicap odds
        :param dnb: str: Parse the double chance odds
        :param dc: str: Parse the double chance odds
        :param bts: str: Parse the both teams to score odds
        :return: A dictionary with the keys: info, 1x2, ou, ah, dnb, dc, bts
        """

        match = dict()
        match["info"] = self._parse_info(page)
        match["1x2"] = self._parse_common(x12)
        match["ou"] = self._parse_over_under(ou)
        match["ah"] = self._parse_over_under(ah)
        match["dnb"] = self._parse_common(dnb)
        match["dc"] = self._parse_common(dc)
        match["bts"] = self._parse_common(bts)

        return match

    @staticmethod
    def _parse_info(page: str) -> dict:
        soup = BeautifulSoup(page, "lxml")
        match_id = None
        for script in soup("script", {"type": "text/javascript"}):
            if "match_init" in script.text:
                match_init_line = script.text[script.text.find("match_init"):]
                start_idx = match_init_line.find("'") + 1
                end_idx = match_init_line[start_idx:].find("'") + start_idx
                match_id = match_init_line[start_idx: end_idx]
                break

        league = soup.find("meta", {"name": "description"})["content"].split(":")[0].strip()
        season = int(soup.find("h1", class_="wrap-section__header__title").a.text.split()[-1].split("/")[0])
        info_block = soup.find("ul", class_="list-details").find_all("li", class_="list-details__item")
        home_team = info_block[0].find("h2").find("a").text.strip()
        away_team = info_block[2].find("h2").find("a").text.strip()
        dt = info_block[1].find("p", class_="list-details__item__date")["data-dt"]
        dt = datetime.strptime(dt, "%d,%m,%Y,%H,%M")
        date = dt.date()
        time = dt.time()
        home_score, away_score = map(int, info_block[1].find("p", class_="list-details__item__score").text.split(":"))

        return {"id": match_id, "league": league, "season": season,
                "home_team": home_team, "away_team": away_team, "date": date,
                "time": time, "score": {"home": home_score, "away": away_score}}

    @staticmethod
    def _parse_common(page: str) -> dict:
        soup = BeautifulSoup(page, "lxml")

        try:
            headers = [header.text for header in soup("th", class_="table-main__detail-odds")]
            coefs = [float(coef["data-odd"]) for coef in soup.find(
                "tfoot").find_all("td", class_="table-main__detail-odds")]
        except AttributeError:
            headers, coefs = [], []

        return {header: coef for header, coef in zip(headers, coefs)}

    @staticmethod
    def _parse_over_under(page: str) -> list[dict]:
        soup = BeautifulSoup(page, "lxml")
        try:
            odd_blocks = soup.find("div", {"id": "odds-content"}).find_all("div", class_="box-overflow")
            headers = [odd_blocks[0].find("th", class_="unsortable table-main__doubleparameter").text]
            headers.extend([header.text for header in odd_blocks[0].find_all("th", class_="table-main__detail-odds")])
            odds = []
            for odd_block in odd_blocks:
                total = odd_block.find("tbody").find("td", class_="table-main__doubleparameter").text
                if len(totals := total.split(",")) > 1:
                    total = (float(totals[0]) + float(totals[1])) / len(totals)

                coefs = [coef["data-odd"] for coef in odd_block.find("tfoot").find_all(
                    "td", class_="table-main__detail-odds")]
                coefs = [float(coef) if coef else None for coef in coefs]
                coefs.insert(0, total)
                odds.append({header: coef for header, coef in zip(headers, coefs)})
        except AttributeError:
            odds = []
        return odds
