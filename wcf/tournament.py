''' tournament.py -- holder of WCF tournament details

    Tournament details are stored and accessed through a single interface.
    Includes both information about the full tournament and individual games,
    depending on the user's needs
'''


from . import game


class Tournament:

    def __init__(self, data):
        self.data = data

    def __getitem__(self, index):
        return self.data[index]

    def convert(self, keep_raw=True):
        self.data = [game.Game(d, keep_raw=keep_raw) for d in self.data]
