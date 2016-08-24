''' wcfapi.py -- Access results database through official means

    The World Curling Federation maintains a results database that can be
    accessed through normal REST means, but requires you to login and append
    your credentials to every request. To ease this, here is a way to access
    the database through official channels.
'''


import json

import requests


class WCF:
    def __init__(self, timeout=1.0):
        self.base = r'http://resultsapi.azurewebsites.net/api'
        self.timeout = timeout

    def load_user(self):
        with open('credentials.json', 'r') as f:
            self.credentials = json.load(f)
        return self  # to chain load_user().connect()

    def connect(self):
        r = requests.post('{}/Authorize'.format(self.base),
                          data=self.credentials,
                          timeout=self.timeout)
        assert r.status_code == requests.codes.ok
        self.token = r.json()

    def get_people(self, surname=None, details=None):
        ''' Get people from the database by identifier

            When searching by 'surname', returns matches that fit the beginning
            of the name (so 'Koe' returns 5 people, not just Kevin Koe)
        '''
        surname = surname if surname else 'none'
        details = details if details else 'none'
        params = {'surname': surname, 'details': details}
        return self._get_param_data('People', params=params)

    def get_draws_by_tournament(self, id):
        return self._get_param_data('Games', params={'tournamentId': id})

    def get_fact(self):
        return self._get_non_param_data('Facts')

    def get_classes(self):
        return self._get_non_param_data('BasicInformation/CompetitionClasses')

    def _get_param_data(self, endpoint, params):
        r = requests.get('{}/{}'.format(self.base, endpoint),
                         params=params,
                         headers={'Authorize': self.token},
                         timeout=self.timeout)
        assert r.status_code == requests.codes.ok
        return r.json()

    def _get_non_param_data(self, endpoint):
        r = requests.get('{}/{}'.format(self.base, endpoint),
                         headers={'Authorize': self.token},
                         timeout=self.timeout)
        assert r.status_code == requests.code.ok
        return r.json()
