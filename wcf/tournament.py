''' tournament.py -- holder of WCF tournament details

    Tournament details are stored and accessed through a single interface.
    Includes both information about the full tournament and individual games,
    depending on the user's needs

    Note: full tournament information not yet present. Requires second argument
    in constructor and a second API call.
'''


from collections.abc import Sequence

from . import game


class Tournament(Sequence):
    def __init__(self, game_data, tourney_data=None):
        self.game_data = game_data
        self.tourney_data = tourney_data
        return self

    def __getitem__(self, index):
        return self.game_data[index]

    def __len__(self):
        return len(self.game_data)

    def convert(self, keep_raw=True):
        self._extract_tournament_data()
        self.game_data = [game.Game(d, keep_raw=keep_raw)
                          for d in self.game_data]

    def _extract_tournament_data(self):
        self.id = self.game_data[0]['TournamentId']
        if self.tourney_data is not None:
            pass
