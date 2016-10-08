''' structure.py -- Storing results in a usable way

    The raw data from games and tournaments kept by the WCF are not the best
    for actually trying to do analysis on. They contain extraneous information
    that would not have an affect on the outcome of analysis and serve no
    purpose for a learning project. The structures contained within aide the
    end user to convert the WCF data into something usable.
'''


from collections import namedtuple
from datetime import datetime
import json


class Tournament:
    def __init__(self, file, *, keep_raw=True):
        self.file = file
        self.keep_raw = keep_raw

    def __iter__(self):
        for g in self.games:
            yield g

    def __getitem__(self, index):
        return self.games[index]

    def load(self):
        with open(self.file, 'r') as f:
            self.data = json.load(f)

    def convert_all(self):
        self.games = []
        for game in self.data:
            _g = Game(game, keep_raw=self.keep_raw)
            self.games.append(_g.convert())
        del self.data


class Game:
    fields = ['TourneyID', 'GameID', 'DrawNumber', 'TotalEnds', 'LSFE', 'Date']
    team_fields = ['Team', 'Score', 'HammerEnds', 'HammerScoringEnds',
                   'HammerScoring2Ends', 'HammerPoints', 'HammerBlanks',
                   'StolenEnds', 'StolenPoints', 'Accuracy']

    def __init__(self, data, *, keep_raw=True):
        self.data = data
        self.teams = []
        self.ends = []
        self.metadata = {}
        self.aggregate_data = None
        self.keep_raw = keep_raw

    def __str__(self):
        if self.aggregate_data:
            data = [*(str(self.metadata[key]) for key in self.fields),
                    *(str(i) for i in self.aggregate_data[self.winner]),
                    *(str(i) for i in self.aggregate_data[not self.winner])]
            return ','.join(data)
        else:
            return 'raw wcf.structure.Game: {}'.format(repr(self))

    def convert(self):
        self._extract_metadata()
        self._extract_ends()
        self._extract_teams()
        self.winner = self._determine_winner()
        if not self.keep_raw:
            self.remove_raw()
        return self

    def _extract_metadata(self):
        self.metadata['tourney_id'] = self.data['TournamentId']
        self.metadata['game_id'] = self.data['Id']
        self.metadata['draw_number'] = self.data['DrawInfo']['DrawNumber']
        self.metadata['total_ends'] = len(self.data['Ends'])
        self.metadata['LSFE'] = self.data['TossWinner']
        self.metadata['date'] = self._convert_date()

    def _convert_date(self):
        date = self.data['DrawInfo']['GameStart']
        date, _ = date.split('T')
        date = [int(d) for d in date.split('-')]
        return datetime(*date)

    def _extract_ends(self):
        for end in self.data['Ends']:
            self.ends.append((end['Team1'], end['Team2']))

    def _extract_teams(self):
        team_data = namedtuple('Team', ['id', 'code', 'name'])
        for team in ('Team1', 'Team2'):
            data = self.data[team]['Team']
            self.teams.append(
                team_data(data['AssociationId'], data['Code'], data['Name'])
            )

    def _determine_winner(self):
        scores = self.data['Team1']['Result'], self.data['Team2']['Result']
        return 0 if scores[0] > scores[1] else 1

    def remove_raw(self):
        del self.data

    def aggregate(self):
        for end in self.ends:
            pass
