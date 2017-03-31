''' game.py -- storage for a single curling game

    Games pulled from the WCF database are saved here for easier access to
    the game information and easier processing
'''


from collections import namedtuple

Team = namedtuple('Team', ['name', 'accuracy', 'result'])
End = namedtuple('End', ['number', 'hammer', 'score_0', 'score_1'])


class Game:

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return '\n'.join(self._make_team_string(i) for i in (0, 1))

    def _make_team_string(self, index):
        try:
            team = self.teams[index]
            ends = ' '.join(str(e[index + 2]) for e in self.ends)
            lsfe = '*' if index == self.lsfe else ' '
            return '{}{} {} | {} | {}'.format(team.name, lsfe, team.accuracy,
                                              ends, team.result)
        except:
            return 'unconverted wcf.Game'

    def convert(self):
        if self.data:
            self._convert_if_available()
        self.winner = 0 if self.teams[0].result > self.teams[1].result else 1
        self.data = None

    def _convert_if_available(self):
        self.lsfe = self.data['TossWinner'] - 1
        self._convert_teams()
        self._convert_ends()
        self.draw = self.data['Round']['Name']

    def _convert_teams(self):
        teams = self.data['Team1'], self.data['Team2']
        self.teams = [Team(t['Team']['Code'], t['Percentage'], t['Result'])
                      for t in teams]

    def _convert_ends(self):
        ends = [(end['Team1'], end['Team2']) for end in self.data['Ends']]
        hammer = self._find_hammer(ends)
        self.ends = [End(i + 1, h, e[0], e[1])
                     for i, (e, h) in enumerate(zip(ends, hammer))]

    def _find_hammer(self, ends):
        hammer = [0] * len(ends)
        hammer[0] = self.lsfe
        for i, end in enumerate(ends[:-1]):
            hammer[i + 1] = self._get_hammer_change(end, hammer[i])
        return hammer

    def _get_hammer_change(self, end, previous):
        if end[0] > end[1]:
            return 1
        elif end[0] < end[1]:
            return 0
        return previous
