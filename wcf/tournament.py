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

    def convert(self):
        self.data = [game.Game(d) for d in self.data]
