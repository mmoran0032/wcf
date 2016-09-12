''' wcf.py -- Access results database through official means

    The World Curling Federation maintains a results database that can be
    accessed through normal REST means, but requires you to login and append
    your credentials to every request. To ease this, here is a way to access
    the database through official channels.

    This class will be limited initially to what I need it to do, and not to
    implement the entire functionality of the WCF's API.
'''


import json
from numbers import Number
from os.path import isfile

import requests


class WCF:
    def __init__(self, *, timeout=10.0, connect=False):
        self.base = r'http://resultsapi.azurewebsites.net/api'
        self.timeout = timeout
        self.token = None
        if connect:
            self.load_and_connect()

    def __bool__(self):
        return self.token is not None

    def __str__(self):
        if self.token is not None:
            _status = '{} ({} s)'.format(self.credentials['Username'],
                                         self.timeout)
        else:
            _status = 'NOT ACTIVE'
        return 'WCF API connection: {}'.format(_status)

    def load_and_connect(self, cred_file='credentials.json'):
        self.cred_file = cred_file
        self._load_user()
        self._connect()

    def _load_user(self):
        with open(self.cred_file, 'r') as f:
            self.credentials = json.load(f)

    def _connect(self):
        r = requests.post('{}/Authorize'.format(self.base),
                          data=self.credentials,
                          timeout=self.timeout)
        assert r.status_code == requests.codes.ok, r.status_code
        self.token = r.json()

    def get_draws_by_tournament(self, id, details='ends'):
        params = {'tournamentId': id, 'details': details}
        return self._get_generic_data('Games', params=params)

    def get_tournaments_by_type(self, id):
        return self._get_generic_data('Tournaments/Type/{}'.format(id))

    def _get_generic_data(self, endpoint, **kwargs):
        r = requests.get('{}/{}'.format(self.base, endpoint),
                         headers={'Authorize': self.token},
                         timeout=self.timeout,
                         **kwargs)
        assert r.status_code == requests.codes.ok, r.status_code
        return r.json()

    @property
    def cred_file(self):
        return self._cred_file

    @cred_file.setter
    def cred_file(self, new_cred_file):
        assert isfile(new_cred_file), 'file does not exist'
        self._cred_file = new_cred_file

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, new_timeout):
        assert isinstance(new_timeout, Number), 'timeout must be a number'
        assert new_timeout > 0, 'timeout must be positive'
        self._timeout = new_timeout
