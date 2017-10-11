''' wcf_scraper.py -- pull web-based results from WCF website

    The World Curling Federation maintains a results database that can be
    accessed through normal REST means, but requires you to login and append
    your credentials to every request. Without credentials, you must scrape
    the website in order to get the results.

    To ease post-processing, the scraper will format the tournament results
    in a similar manner to the official API. We will build out the JSON
    "response" to return to our calling program.
'''


from bs4 import BeautifulSoup
import requests


class Scraper:
    def __init__(self, *, timeout=10.0):
        self.base = r'http://results.worldcurling.org/Championship'
        self.timeout = timeout

    def get_draws_by_tournament(self, id_):
        r = self._scrape_from_wcf(id_)
        return self._format_response(r, id_)

    def _scrape_from_wcf(self, id_):
        params = {'tournamentId': id_, 'associationId': 0, 'drawNumber': 0}
        r = requests.get(f'{self.base}/DisplayResults',
                         timeout=self.timeout,
                         params=params)
        assert r.status_code == requests.codes.ok, r.status_code
        return r

    def _format_response(self, r, id_):
        soup = BeautifulSoup(r.text, 'html.parser')
        games = soup.find_all('table', class_='game-table')
        return [self._format_single_game(g, id_) for g in games]

    def _format_single_game(self, game, id_):
        ''' build out single game dict as below'''
        _toss_winner = self._extract_hammer(game)
        _ends = self._extract_ends(game)
        _round = self._extract_round(game)
        _team1, _team2 = self._extract_teams(game)
        return dict(tournamentId=id_,
                    Id=0,
                    Round=dict(Abbreviation=_round),
                    TossWinner=_toss_winner,
                    Ends=_ends,
                    Team1=_team1,
                    Team2=_team2)

    def _extract_hammer(self, game):
        _hammer = game.find_all('td', class_='game-hammer')
        _hammer = [entry.text.strip() for entry in _hammer]
        return _hammer.index('*') + 1  # correct indexing to match WCF database

    def _extract_ends(self, game):
        _ends = game.find_all('tr', class_=None)
        new_ends = []
        for row in _ends:
            scores = row.find_all('td', 'game-end10')
            scores = [d.text.strip().replace('X', '') for d in scores]
            new_ends.append([int(d) for d in scores if d])
        paired = list(zip(*new_ends))
        return [dict(Team1=e[0], Team2=e[1]) for e in paired]

    def _extract_round(self, game):
        return game.find('th', class_='game-header').text.strip()[0]

    def _extract_teams(self, game):
        _results = game.find_all('td', class_='game-total')
        _results = [int(data.text.strip()) for data in _results]
        _names = game.find_all('td', class_='game-team')
        _names = [self._reformat_name(name.text.strip()) for name in _names]
        _team1 = dict(Result=_results[0],
                      Percentage=0,
                      Team=dict(Code=_names[0]))
        _team2 = dict(Result=_results[1],
                      Percentage=0,
                      Team=dict(Code=_names[1]))
        return _team1, _team2

    def _reformat_name(self, name):
        ''' convert country names to (rough) codes '''
        name = name.replace('of', '').upper().split()
        if len(name) > 2:
            return ''.join(entry[0] for entry in name)
        return name[0][:3]
