''' game.py -- storage for a single curling game

    Games pulled from the WCF database are saved here for easier access to
    the game information and easier processing
'''


from collections import namedtuple

team = namedtuple('Team', ['name', 'accuracy', 'result'])


class Game:

    def __init__(self, data):
        self.data = data
        self.convert()

    def __str__(self):
        return '\n'.join(self._make_team_string(i) for i in (0, 1))

    def _make_team_string(self, index):
        team = self.teams[index]
        ends = ' '.join(str(e) for e in self.ends[index])
        lsfe = '*' if index == self.hammer else ' '
        return '{}{} {} | {} | {}'.format(team.name, lsfe, team.accuracy,
                                          ends, team.result)

    def convert(self):
        self._convert_teams()
        self._convert_ends()
        self.hammer = self.data['TossWinner'] - 1
        self.winner = 0 if self.teams[0].result > self.teams[1].result else 1

    def _convert_teams(self):
        teams = self.data['Team1'], self.data['Team2']
        self.teams = [team(t['Team']['Code'], t['Percentage'], t['Result'])
                      for t in teams]

    def _convert_ends(self):
        self.ends = [[end[team] for end in self.data['Ends']]
                     for team in ['Team1', 'Team2']]
