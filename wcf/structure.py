''' structure.py -- Storing results in a usable way

    The raw data from games and tournaments kept by the WCF are not the best
    for actually trying to do analysis on. They contain extraneous information
    that would not have an affect on the outcome of analysis and serve no
    purpose for a learning project. The structures contained within aide the
    end user to convert the WCF data into something usable.
'''


from datetime import datetime
import json


class Tournament:
    def __init__(self, file, *, keep_raw=True):
        self.file = file
        self.keep_raw = keep_raw

    def load(self):
        with open(self.file, 'r') as f:
            self.data = json.load(f)

    def convert(self):
        self.games = [Game(g) for g in self.data]
        self.games = [g.convert() for g in self.games]
        if not self.keep_raw:
            del self.data


class Game:
    fields = ['TourneyID', 'GameID', 'DrawNumber', 'TotalEnds', 'LSFE',
              'WTeam', 'WScore', 'WHammerEnds', 'WHammerScoringEnds',
              'WHammer2ScoringEnds', 'WHammerPoints', 'WHammerBlanks',
              'WStolenEnds', 'WStolenPoints', 'WAccuracy',
              'LTeam', 'LScore', 'LHammerEnds', 'LHammerScoringEnds',
              'LHammer2ScoringEnds', 'LHammerPoints', 'LHammerBlanks',
              'LStolenEnds', 'LStolenPoints', 'LAccuracy']

    def __init__(self, data, *, keep_raw=True):
        self.data = data
        self.teams = []
        self.ends = []
        self.metadata = {}
        self.aggregate = {}
        self.keep_raw = keep_raw

    def convert(self):
        self._extract_metadata()
        self._extract_ends()
        self._extrat_teams()
        if not self.keep_raw:
            del self.data

    def _extract_metadata(self):
        self.metadata['TourneyID'] = self.data['TournamentId']
        self.metadata['GameID'] = self.data['Id']
        self.metadata['DrawNumber'] = self.data['DrawInfo']['DrawNumber']
        self.metadata['TotalEnds'] = len(self.data['Ends'])
        self.metadata['LSFE'] = self.data['TossWinner']
        self.metadata['Date'] = self._convert_date()

    def _convert_date(self):
        date = self.data['DrawInfo']['GameStart']
        date, _ = date.split('T')
        date = [int(d) for d in date.split('-')]
        return datetime(*date)

    def _extract_ends(self):
        ends = self.data['Ends']
        for end in ends:
            self.ends.append((end['Team1'], end['Team2']))

    def _extrat_teams(self):
        for team in ('Team1', 'Team2'):
            pass
