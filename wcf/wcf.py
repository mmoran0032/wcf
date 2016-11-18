''' wcf.py -- Access results database through official means

    The World Curling Federation maintains a results database that can be
    accessed through normal REST means, but requires you to login and append
    your credentials to every request. To ease this, here is a way to access
    the database through official channels.

    This class will be limited initially to what I need it to do, and not to
    implement the entire functionality of the WCF's API.
'''


import json

import requests


class WCF:

    def __init__(self, *, timeout=10.0):
        self.base = r'http://resultsapi.azurewebsites.net/api'
        self.timeout = timeout
        self.token = None

    def __bool__(self):
        return self.token is not None

    def load_and_connect(self, cred_file=None):
        self._load_user(cred_file)
        self._connect()

    def _load_user(self, cred_file):
        cred_file = cred_file or 'credentials.json'
        with open(cred_file, 'r') as f:
            self.credentials = json.load(f)

    def _connect(self):
        r = requests.post('{}/Authorize'.format(self.base),
                          data=self.credentials, timeout=self.timeout)
        self.token = self._check_and_return(r)

    def get_draws_by_tournament(self, id, *, details='ends'):
        params = {'tournamentId': id, 'details': details}
        return self._access_wcf('Games', params=params)

    def get_tournaments_by_type(self, id):
        return self._access_wcf('Tournaments/Type/{}'.format(id))

    def _access_wcf(self, endpoint, **kwargs):
        r = requests.get('{}/{}'.format(self.base, endpoint),
                         headers={'Authorize': self.token},
                         timeout=self.timeout,
                         **kwargs)
        return self._check_and_return(r)

    def _check_and_return(self, r):
        assert r.status_code == requests.codes.ok, r.status_code
        return r.json()
