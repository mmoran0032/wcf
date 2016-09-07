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
    def __init__(self, timeout=1.0, connect=False):
        self.base = r'http://resultsapi.azurewebsites.net/api'
        self.timeout = timeout
        self.token = None
        if connect:
            self.load_and_connect()

    def __bool__(self):
        return self.token is not None

    def __str__(self):
        if self.token is not None:
            _status = '{} ({} s)'.format(self.credentials['UserName'],
                                         self.timeout)
        else:
            _status = 'NOT ACTIVE'
        return 'WCF API connection: {}'.format(_status)

    def load_and_connect(self, filename='credentials.json'):
        self._load_user(filename)
        self._connect()

    def _load_user(self, filename):
        with open(filename, 'r') as f:
            self.credentials = json.load(f)

    def _connect(self):
        r = requests.post('{}/Authorize'.format(self.base),
                          data=self.credentials,
                          timeout=self.timeout)
        assert r.status_code == requests.codes.ok, 'bad response code'
        self.token = r.json()

    def get_draws_by_tournament(self, id, details='ends'):
        params = {'tournamentId': id, 'details': details}
        return self._get_generic_data('Games', params=params)

    def _get_generic_data(self, endpoint, **kwargs):
        r = requests.get('{}/{}'.format(self.base, endpoint),
                         headers={'Authorize': self.token},
                         timeout=self.timeout,
                         **kwargs)
        assert r.status_code == requests.codes.ok, 'bad response code'
        return r.json()
